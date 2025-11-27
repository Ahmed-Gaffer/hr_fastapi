import math
import re
import pandas as pd
from datetime import date, datetime

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
