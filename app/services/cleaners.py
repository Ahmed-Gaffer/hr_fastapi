# app/services/cleaners.py
import pandas as pd

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

def clean_employee_data(stream) -> pd.DataFrame:
    df = pd.read_excel(stream)
    df = _normalize_columns(df)

    # توحيد التواريخ
    if "hire_date" in df.columns:
        df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # الرقم القومي
    if "national_id" in df.columns:
        df["national_id"] = df["national_id"].astype(str).str.strip().replace({"nan": "غير متوفر"}).fillna("غير متوفر")

    # التأمين
    if "insurance_status" in df.columns:
        df["insurance_status"] = df["insurance_status"].replace({
            "نعم": "مؤمن",
            "لا": "غير مؤمن"
        }).fillna("غير مؤمن")

    # الفئة
    if "employee_category" in df.columns:
        df["employee_category"] = df["employee_category"].fillna("غير محدد")

    # حالة العمل
    if "work_status" in df.columns:
        df["work_status"] = df["work_status"].replace({
            "يعمل": "يعمل",
            "اجاوه بدون مرتب": "غير نشط"
        }).fillna("غير نشط")

    return df

def clean_attendance_data(stream) -> pd.DataFrame:
    df = pd.read_excel(stream)
    df = _normalize_columns(df)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    return df

def clean_salary_data(stream) -> pd.DataFrame:
    df = pd.read_excel(stream)
    df = _normalize_columns(df)
    if "salary_date" in df.columns:
        df["salary_date"] = pd.to_datetime(df["salary_date"], errors="coerce")
    return df
