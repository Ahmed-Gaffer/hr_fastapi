# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\helpers.py
# File Name: helpers.py
# -----------------------------------------



import math
import pandas as pd
from datetime import date, datetime

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

def clean_value(value):
    if value is None: return None
    if isinstance(value, float) and math.isnan(value): return None
    if isinstance(value, float) and value.is_integer(): return str(int(value))
    s = str(value).strip()
    return s or None

def arabic_to_bool(value):
    if value is None: return None
    s = str(value).strip()
    return True if s == "نعم" else False if s == "لا" else None

def parse_date(value):
    try:
        if isinstance(value, str): return pd.to_datetime(value).date()
        if isinstance(value, (datetime, date)): return value
    except: return None

def clean_employee_data(stream) -> pd.DataFrame:
    df = pd.read_excel(stream)
    df = _normalize_columns(df)

    # توحيد التواريخ
    if "hire_date" in df.columns:
        df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # الرقم القومي
    if "national_id" in df.columns:
        df["national_id"] = df["national_id"].apply(clean_value).fillna("غير متوفر")

    # التأمين
    if "insurance_status" in df.columns:
        df["insurance_status"] = df["insurance_status"].apply(
            lambda v: "مؤمن" if str(v).strip() == "نعم" else "غير مؤمن"
        )

    # الفئة
    if "employee_category" in df.columns:
        df["employee_category"] = df["employee_category"].fillna("غير محدد")

    # حالة العمل
    if "work_status" in df.columns:
        df["work_status"] = df["work_status"].replace({
            "يعمل": "يعمل",
            "اجاوه بدون مرتب": "اجازة",
            "لا يعمل": "موقوف"
        }).fillna("موقوف")

    return df