# app/services/imports/employees.py
import io
import pandas as pd
from sqlmodel import Session, select
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.services.cleaners import clean_employee_data  # ← إضافة

class EmployeeImporter:
    def run(self, session: Session, stream: bytes, commit: bool, allow_create_tenant: bool):
        # قراءة + تنظيف قبل أي شيء
        df = clean_employee_data(io.BytesIO(stream))

        required = ["code", "name"]
        for col in required:
            if col not in df.columns:
                return {"status": "error", "detail": f"عمود {col} غير موجود"}

        imported, skipped = 0, 0
        report_rows = []

        for _, row in df.iterrows():
            code = str(row.get("code")).strip()
            name = str(row.get("name")).strip()
            department = row.get("department")
            company_name = row.get("company_name")

            tenant = None
            if company_name:
                tenant = session.exec(select(Tenant).where(Tenant.name == company_name)).first()
                if not tenant and allow_create_tenant:
                    tenant = Tenant(name=company_name, code=f"auto-{company_name}")
                    session.add(tenant)
                    session.commit()
                    session.refresh(tenant)

            if not tenant:
                skipped += 1
                report_rows.append({"code": code, "reason": "لا توجد شركة/company_name"})
                continue

            exists = session.exec(
                select(Employee).where(Employee.tenant_id == tenant.id, Employee.code == code)
            ).first()
            if exists:
                skipped += 1
                report_rows.append({"code": code, "reason": "كود مكرر"})
                continue

            emp = Employee(
                tenant_id=tenant.id,
                code=code,
                name=name,
                base_salary=float(row.get("base_salary") or 0),
                department=department,
                status="نشط",
            )
            session.add(emp)
            imported += 1

        if commit:
            session.commit()

        return {"status": "ok", "imported": imported, "skipped": skipped, "rows": report_rows}
