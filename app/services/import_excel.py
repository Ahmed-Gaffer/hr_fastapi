# دالة استيراد الموظفين من ملف Excel
import pandas as pd
from sqlmodel import Session
from app.database import engine
from app.models.employee import Employee

# دالة تحويل "نعم"/"لا" إلى True/False
def arabic_to_bool(value):
    return str(value).strip() == "نعم"

def import_employees_from_excel(excel_path: str):
    df = pd.read_excel(excel_path)

    with Session(engine) as session:
        for _, row in df.iterrows():
            emp = Employee(
                legacy_code=row.get("legacy_code"),
                full_name=row.get("full_name"),
                title=row.get("title"),
                phone=row.get("phone"),
                hire_date=row.get("hire_date"),
                site_name=row.get("site_name"),
                company_name=row.get("company_name"),
                cost_center=row.get("cost_center"),
                insured=arabic_to_bool(row.get("insured")),
                overnight=arabic_to_bool(row.get("overnight"))
            )
            session.add(emp)
        session.commit()

    print("✅ تم استيراد الموظفين بنجاح")
