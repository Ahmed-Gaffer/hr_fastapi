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
    def run(self, session: Session, stream: bytes, commit: bool, allow_create_tenant: bool):
        try:
            df = clean_employee_data(io.BytesIO(stream))
            print("📄 Excel columns:", df.columns.tolist())

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

                    tenant = None
                    if company_name:
                        tenant = session.exec(
                            select(Tenant).where(Tenant.name == company_name)
                        ).first()
                        if not tenant and allow_create_tenant:
                            tenant = Tenant(name=company_name, code=f"auto-{company_name}")
                            session.add(tenant)
                            session.flush()

                    if not tenant:
                        skipped += 1
                        report_rows.append({"row": idx, "reason": "tenant not found"})
                        continue

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
