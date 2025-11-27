import io
from sqlmodel import Session, select
from datetime import datetime
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.services.cleaners import clean_employee_data

class EmployeeImporter:
    def run(self, session: Session, stream: bytes, commit: bool, allow_create_tenant: bool):
        # قراءة + تنظيف البيانات
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
            company_name = row.get("company_name")

            # البحث عن الشركة
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

            # منع التكرار
            exists = session.exec(
                select(Employee).where(Employee.tenant_id == tenant.id, Employee.code == code)
            ).first()
            if exists:
                skipped += 1
                report_rows.append({"code": code, "reason": "كود مكرر"})
                continue

            # إنشاء الموظف بكامل الأعمدة بعد التنظيف
            emp = Employee(
                tenant_id=tenant.id,
                code=code,
                name=name,
                national_id=row.get("national_id"),
                job_title=row.get("job_title"),
                hire_date=row.get("hire_date"),
                company_name=company_name,
                site_name=row.get("site_name"),
                cost_center=row.get("cost_center"),
                insurance_status=row.get("insurance_status"),
                employee_category=row.get("employee_category"),
                work_status=row.get("work_status"),
                base_salary=float(row.get("base_salary") or 0),
                status=row.get("work_status") or "نشط",
                department=row.get("department"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(emp)
            imported += 1

        if commit:
            session.commit()

        return {"status": "ok", "imported": imported, "skipped": skipped, "rows": report_rows}
