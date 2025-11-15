import pandas as pd
import math
from sqlmodel import Session, select
from app.database import engine
from app.models.employee import Employee

def clean_value(value):
    """تنظيف القيم من NaN والفراغات"""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    value = str(value).strip()
    if value.lower() == "nan" or value == "":
        return None
    return value

def arabic_to_bool(value):
    return str(value).strip() == "نعم"

def import_employees_from_excel(excel_path: str):
    df = pd.read_excel(excel_path)

    with Session(engine) as session:
        for _, row in df.iterrows():
            # الأعمدة الأساسية (استخدام clean_value)
            national_id = clean_value(row.get("national_id"))
            legacy_code = clean_value(row.get("legacy_code"))

            # تحديد المفتاح الأساسي حسب الأولوية
            identifier = None
            if national_id:
                identifier = ("national_id", national_id)
            elif legacy_code:
                identifier = ("legacy_code", legacy_code)

            # البحث عن الموظف
            existing = None
            if identifier:
                existing = session.exec(
                    select(Employee).where(getattr(Employee, identifier[0]) == identifier[1])
                ).first()

            if existing:
                # تحديث بيانات الموظف الموجود
                existing.full_name = row.get("full_name")
                existing.title = row.get("title")
                existing.phone = row.get("phone")
                existing.status = row.get("status", "active")
                existing.hire_date = row.get("hire_date")
                existing.site_name = row.get("site_name")
                existing.company_name = row.get("company_name")
                existing.cost_center = row.get("cost_center")
                existing.insured = arabic_to_bool(row.get("insured"))
                existing.overnight = arabic_to_bool(row.get("overnight"))
                existing.site_id = row.get("site_id")
            else:
                if not national_id and not legacy_code:
                    print(f"❌ الصف مرفوض: الموظف {row.get('full_name')} بدون رقم قومي أو كود قديم")
                    continue

                # إضافة موظف جديد
                emp = Employee(
                    national_id=national_id,
                    legacy_code=legacy_code,
                    full_name=row.get("full_name"),
                    title=row.get("title"),
                    phone=row.get("phone"),
                    status=row.get("status", "active"),
                    hire_date=row.get("hire_date"),
                    site_name=row.get("site_name"),
                    company_name=row.get("company_name"),
                    cost_center=row.get("cost_center"),
                    insured=arabic_to_bool(row.get("insured")),
                    overnight=arabic_to_bool(row.get("overnight")),
                    site_id=row.get("site_id"),
                )
                session.add(emp)

        session.commit()

    print("✅ تم الاستيراد بنجاح (بالأولوية: national_id → legacy_code → employee_id الداخلي)")
