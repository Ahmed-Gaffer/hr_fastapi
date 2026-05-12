# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\cleaners.py
# File Name: cleaners.py
# -----------------------------------------



import math
import pandas as pd
from datetime import date, datetime

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """توحيد أسماء الأعمدة كلها إلى lowercase وباستبدال الفراغات والرموز بـ underscores."""
    normalized = []
    for c in df.columns:
        header = str(c).strip().lower()
        header = header.replace(" ", "_")
        header = header.replace("/", "_")
        header = header.replace("-", "_")
        header = header.replace("\\", "_")
        header = header.replace(".", "_")
        header = header.replace("__", "_")
        normalized.append(header)
    df.columns = normalized
    return df

def clean_value(value):
    """تنظيف أي قيمة: تحويل NaN إلى None، وتحويل الأرقام إلى نصوص لو محتاج"""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    s = str(value).strip()
    return s or None

def arabic_to_bool(value):
    """تحويل نعم/لا إلى Boolean"""
    if value is None:
        return None
    s = str(value).strip()
    return True if s == "نعم" else False if s == "لا" else None

def parse_date(value):
    """تحويل النص أو التاريخ إلى datetime.date"""
    try:
        if isinstance(value, str):
            return pd.to_datetime(value, errors="coerce").date()
        if isinstance(value, (datetime, date)):
            return value
    except:
        return None

def clean_employee_data(stream) -> pd.DataFrame:
    """تنظيف بيانات الموظفين قبل الاستيراد"""
    df = pd.read_excel(stream)
    df = _normalize_columns(df)

    # توحيد التواريخ
    if "hire_date" in df.columns:
        df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce").dt.date

    # الرقم القومي
    if "national_id" in df.columns:
        df["national_id"] = df["national_id"].apply(clean_value).fillna("غير متوفر")

    # التأمين
    if "insurance_status" in df.columns:
        df["insurance_status"] = df["insurance_status"].replace({
            "نعم": "مؤمن",
            "لا": "غير مؤمن"
        }).fillna("غير مؤمن")

    # الفئة
    if "employee_category" in df.columns:
        df["employee_category"] = df["employee_category"].fillna("غير محدد")

    # حالة العمل → توحيد قيم work_status
    if "work_status" in df.columns:
        df["work_status"] = df["work_status"].apply(clean_value)
        df["work_status"] = df["work_status"].replace({
            "يعمل": "يعمل",
            "نشط": "يعمل",
            "لا يعمل": "موقوف",
            "موقوف": "موقوف",
            "اجازة بدون مرتب": "اجازة بدون مرتب",
            "اجاوه بدون مرتب": "اجازة بدون مرتب",
            "إجازة بدون مرتب": "اجازة بدون مرتب",
        }).fillna(df["work_status"])

    return df

def clean_attendance_data(stream) -> pd.DataFrame:
    """تنظيف بيانات الحضور"""
    df = pd.read_excel(stream)
    df = _normalize_columns(df)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    return df

def clean_salary_data(stream) -> pd.DataFrame:
    """تنظيف بيانات الرواتب"""
    df = pd.read_excel(stream)
    df = _normalize_columns(df)
    if "salary_date" in df.columns:
        df["salary_date"] = pd.to_datetime(df["salary_date"], errors="coerce").dt.date
    return df