import io
from sqlmodel import Session, select
from datetime import datetime
from app.models.employee import Employee
from app.models.tenant import Tenant
from app.models.site import Site
from app.models.cost_center import Project
from app.models.department import Department
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

            # 🔹 البحث عن الشركة (Tenant)
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

            # 🔹 منع التكرار
            exists = session.exec(
                select(Employee).where(Employee.tenant_id == tenant.id, Employee.code == code)
            ).first()
            if exists:
                skipped += 1
                report_rows.append({"code": code, "reason": "كود مكرر"})
                continue

            # 🔹 الموقع (Site)
            site = None
            site_name = row.get("site_name")
            if site_name:
                site = session.exec(
                    select(Site).where(Site.name == site_name, Site.tenant_id == tenant.id)
                ).first()
                if not site:
                    site = Site(name=site_name, tenant_id=tenant.id)
                    session.add(site)
                    session.commit()
                    session.refresh(site)

            # 🔹 مركز التكلفة / المشروع (Project)
            project = None
            cost_center_name = row.get("cost_center")
            if cost_center_name:
                project = session.exec(
                    select(Project).where(Project.name == cost_center_name, Project.tenant_id == tenant.id)
                ).first()
                if not project:
                    project = Project(
                        name=cost_center_name,
                        tenant_id=tenant.id,
                        site_id=site.id if site else None
                    )
                    session.add(project)
                    session.commit()
                    session.refresh(project)

            # 🔹 القسم (Department)
            department = None
            dept_name = row.get("department")
            if dept_name:
                department = session.exec(
                    select(Department).where(Department.name == dept_name, Department.tenant_id == tenant.id)
                ).first()
                if not department:
                    department = Department(name=dept_name, tenant_id=tenant.id)
                    session.add(department)
                    session.commit()
                    session.refresh(department)

            # 🔹 إنشاء الموظف وربطه بالـ IDs
            emp = Employee(
                tenant_id=tenant.id,
                site_id=site.id if site else None,
                project_id=project.id if project else None,
                department_id=department.id if department else None,
                code=code,
                name=name,
                national_id=row.get("national_id"),
                job_title=row.get("job_title"),
                hire_date=row.get("hire_date"),
                insurance_status=row.get("insurance_status"),
                employee_category=row.get("employee_category"),
                work_status=row.get("work_status"),
                base_salary=float(row.get("base_salary") or 0),
                status=row.get("work_status") or "نشط",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(emp)
            imported += 1

        if commit:
            session.commit()

        return {"status": "ok", "imported": imported, "skipped": skipped, "rows": report_rows}
