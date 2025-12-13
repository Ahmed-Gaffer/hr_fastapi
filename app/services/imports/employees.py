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
from app.models.department import Department
from app.services.cleaners import clean_employee_data


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

                    code = str(row.get("code")).strip()
                    name = str(row.get("name")).strip()
                    company_name = row.get("company_name")

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

                    site = None
                    if row.get("site_name"):
                        site = session.exec(
                            select(Site).where(
                                Site.name == row.get("site_name"),
                                Site.tenant_id == tenant.id
                            )
                        ).first()

                    project = None
                    if row.get("cost_center"):
                        project = session.exec(
                            select(Project).where(
                                Project.name == row.get("cost_center"),
                                Project.tenant_id == tenant.id
                            )
                        ).first()

                    department = None
                    if row.get("department"):
                        department = session.exec(
                            select(Department).where(
                                Department.name == row.get("department"),
                                Department.tenant_id == tenant.id
                            )
                        ).first()

                    emp = Employee(
                        tenant_id=tenant.id,
                        site_id=site.id if site else None,
                        project_id=project.id if project else None,
                        department_id=department.id if department else None,
                        code=code,
                        name=name,
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
