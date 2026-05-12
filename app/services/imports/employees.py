# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\imports\employees.py
# File Name: employees.py
# -----------------------------------------



# app/services/imports/employees.py

import io
import traceback
from datetime import datetime
from sqlmodel import Session, select

from app.models.employee import Employee
from app.models.tenant import Tenant
from app.models.site import Site
from app.models.project import Project
from app.models.cost_center import CostCenter
from app.models.department import Department
from app.services.cleaners import clean_employee_data, clean_value
from app.services.headers import EMPLOYEE_hEADERS


def _value(row, column: str):
    if column not in row:
        return None
    return clean_value(row.get(column))


def _get_or_create(session: Session, model, defaults: dict | None = None, **filters):
    item = session.exec(select(model).filter_by(**filters)).first()
    if item:
        return item

    item = model(**filters, **(defaults or {}))
    session.add(item)
    session.flush()
    return item


class EmployeeImporter:
    def run(self, session: Session, stream: bytes, commit: bool, allow_create_tenant: bool, current_tenant: Tenant):
        try:
            df = clean_employee_data(io.BytesIO(stream))
            print("📄 Raw Excel columns:", df.columns.tolist())
            df.rename(columns={k: v for k, v in EMPLOYEE_hEADERS.items() if k in df.columns}, inplace=True)
            print("📄 Excel columns after rename:", df.columns.tolist())
            print(f"📊 Total rows in Excel: {len(df)}")

            required = ["code", "name"]
            for col in required:
                if col not in df.columns:
                    raise ValueError(f"عمود {col} غير موجود")

            imported, skipped = 0, 0
            report_rows = []

            for idx, row in df.iterrows():
                try:
                    print(f"➡️ Processing row {idx}: {row.to_dict()}")

                    code = _value(row, "code")
                    name = _value(row, "name")
                    company_name = _value(row, "company_name")

                    if not code or not name:
                        skipped += 1
                        report_rows.append({"row": idx, "reason": "missing code or name"})
                        print(f"⚠️ Skipped row {idx}: missing code or name")
                        continue

                    tenant = current_tenant  # استخدم الشركة الحالية دائمًا لضمان ظهور البيانات في البحث

                    exists = session.exec(
                        select(Employee).where(
                            Employee.tenant_id == tenant.id,
                            Employee.code == code
                        )
                    ).first()
                    if exists:
                        skipped += 1
                        continue

                    site_name = _value(row, "site_name")
                    cost_center_name = _value(row, "cost_center")
                    department_name = _value(row, "department")

                    site = None
                    if site_name:
                        site = _get_or_create(
                            session,
                            Site,
                            tenant_id=tenant.id,
                            name=site_name,
                        )

                    project = None
                    cost_center = None
                    if cost_center_name:
                        project = _get_or_create(
                            session,
                            Project,
                            tenant_id=tenant.id,
                            name=cost_center_name,
                            defaults={"site_id": site.id if site else None},
                        )
                        if site and project.site_id is None:
                            project.site_id = site.id
                            session.add(project)

                        cost_center = _get_or_create(
                            session,
                            CostCenter,
                            project_id=project.id,
                            name=cost_center_name,
                            defaults={
                                "tenant_id": tenant.id,
                                "site_id": site.id if site else None,
                            },
                        )
                        if site and cost_center.site_id is None:
                            cost_center.site_id = site.id
                            session.add(cost_center)

                    department = None
                    if department_name:
                        department = _get_or_create(
                            session,
                            Department,
                            tenant_id=tenant.id,
                            name=department_name,
                        )

                    work_status = _value(row, "work_status")
                    status_value = _value(row, "status")
                    employee_category = _value(row, "employee_category")
                    insurance_status = _value(row, "insurance_status")

                    if status_value:
                        status_value = status_value.strip()
                        status_value = {
                            "ACTIVE": "نشط",
                            "SUSPENDED": "موقوف",
                            "TERMINATED": "منتهي",
                            "active": "نشط",
                            "suspended": "موقوف",
                            "terminated": "منتهي",
                        }.get(status_value, status_value)

                    if not status_value and work_status:
                        status_map = {
                            "يعمل": "نشط",
                            "نشط": "نشط",
                            "اجازة بدون مرتب": "موقوف",
                            "اجاوه بدون مرتب": "موقوف",
                            "إجازة بدون مرتب": "موقوف",
                            "اجازة": "موقوف",
                            "إجازة": "موقوف",
                            "لا يعمل": "موقوف",
                            "موقوف": "موقوف",
                        }
                        status_value = status_map.get(work_status, "نشط")

                    if not status_value:
                        status_value = "نشط"

                    emp = Employee(
                        tenant_id=tenant.id,
                        site_id=site.id if site else None,
                        cost_center_id=cost_center.id if cost_center else None,
                        department_id=department.id if department else None,
                        code=code,
                        name=name,
                        national_id=_value(row, "national_id"),
                        job_title=_value(row, "job_title"),
                        hire_date=row.get("hire_date") if "hire_date" in row else None,
                        employee_category=employee_category,
                        insurance_status=insurance_status,
                        work_status=work_status,
                        status=status_value,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )

                    session.add(emp)
                    imported += 1

                except Exception:
                    print(f"❌ Error in row {idx}")
                    traceback.print_exc()
                    skipped += 1

            if commit:
                session.commit()

            print(f"✅ Import summary: {imported} imported, {skipped} skipped, total processed: {imported + skipped}")

            return {
                "status": "ok",
                "imported": imported,
                "skipped": skipped,
                "rows": report_rows
            }

        except Exception:
            print("🔥 Fatal error during employee import")
            traceback.print_exc()
            session.rollback()
            raise
