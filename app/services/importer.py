# app/services/importer.py
import re
import math
import pandas as pd
from io import BytesIO
from datetime import date, datetime
from sqlmodel import Session, select
from app.models.tenant import Tenant
from app.models.employee import Employee
from app.models.salary import SalaryRecord
from app.services.headers import EMPLOYEE_HEADERS, SALARY_HEADERS

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

class Importer:
    def __init__(self, session: Session, tenant: Tenant):
        self.session = session
        self.tenant = tenant

    def _normalize_headers(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        df.columns = [str(c).strip().lower() for c in df.columns]
        df.rename(columns={k: v for k, v in mapping.items() if k in df.columns}, inplace=True)
        return df

    def import_employees(self, stream: BytesIO, commit: bool = True) -> dict:
        report = {"added": 0, "updated": 0, "rejected": 0, "errors": [], "warnings": [], "status": "pending"}
        try:
            df = pd.read_excel(stream, dtype={"national_id": str, "legacy_code": str})
            df = self._normalize_headers(df, EMPLOYEE_HEADERS)

            for idx, row in df.iterrows():
                national_id = clean_value(row.get("national_id"))
                legacy_code = clean_value(row.get("legacy_code"))
                full_name   = clean_value(row.get("full_name"))

                identifier = ("national_id", national_id) if national_id else ("legacy_code", legacy_code) if legacy_code else None
                if not identifier:
                    report["rejected"] += 1
                    report["warnings"].append(f"صف #{idx}: بدون رقم قومي أو كود قديم — الاسم: {full_name}")
                    continue

                existing = self.session.exec(
                    select(Employee).where(getattr(Employee, identifier[0]) == identifier[1])
                ).first()

                if existing:
                    existing.full_name   = full_name
                    existing.title       = clean_value(row.get("title"))
                    existing.phone       = clean_value(row.get("phone"))
                    existing.status      = clean_value(row.get("status")) or "active"
                    existing.hire_date   = parse_date(row.get("hire_date"))
                    existing.site_name   = clean_value(row.get("site_name"))
                    existing.company_name= clean_value(row.get("company_name"))
                    existing.cost_center = clean_value(row.get("cost_center"))
                    existing.insured     = arabic_to_bool(row.get("insured"))
                    existing.overnight   = arabic_to_bool(row.get("overnight"))
                    existing.site_id     = clean_value(row.get("site_id"))
                    report["updated"] += 1
                else:
                    emp = Employee(
                        tenant_id=self.tenant.id if hasattr(self.tenant, "id") else None,
                        national_id=national_id,
                        legacy_code=legacy_code,
                        full_name=full_name,
                        title=clean_value(row.get("title")),
                        phone=clean_value(row.get("phone")),
                        status=clean_value(row.get("status")) or "active",
                        hire_date=parse_date(row.get("hire_date")),
                        site_name=clean_value(row.get("site_name")),
                        company_name=clean_value(row.get("company_name")),
                        cost_center=clean_value(row.get("cost_center")),
                        insured=arabic_to_bool(row.get("insured")),
                        overnight=arabic_to_bool(row.get("overnight")),
                        site_id=clean_value(row.get("site_id")),
                    )
                    self.session.add(emp)
                    report["added"] += 1

            if commit:
                self.session.commit()
                report["status"] = "success"
            else:
                self.session.rollback()
                report["status"] = "dry-run"
        except Exception as e:
            try: self.session.rollback()
            except: pass
            report["status"] = "failed"
            report["errors"].append(str(e))
        return report

    def import_salaries(self, stream: BytesIO, commit: bool = True) -> dict:
        report = {"imported": 0, "errors": [], "warnings": [], "status": "pending"}
        try:
            df = pd.read_excel(stream)
            df = self._normalize_headers(df, SALARY_HEADERS)

            # تحقق من وجود أعمدة أساسية
            required = ["name", "salary_date", "base_salary", "net_salary"]
            missing = [c for c in required if c not in df.columns]
            if missing:
                report["status"] = "failed"
                report["errors"].append(f"أعمدة أساسية ناقصة: {', '.join(missing)}")
                return report

            seen = set()  # (identifier, year, month)
            for idx, row in df.iterrows():
                name = clean_value(row.get("name"))
                if not name:
                    report["errors"].append(f"صف #{idx}: الاسم مفقود")
                    continue

                raw_date = row.get("salary_date")
                sdate = parse_date(raw_date)
                if not sdate:
                    # دعم نصوص تاريخ مختلفة بسرعة
                    try:
                        sdate = datetime.strptime(str(raw_date).strip(), "%Y/%m/%d").date()
                    except:
                        try:
                            sdate = datetime.strptime(str(raw_date).strip(), "%Y-%m-%d").date()
                        except:
                            m = re.findall(r"\d{4}", str(raw_date))
                            if m:
                                sdate = datetime(int(m[0]), 1, 1).date()
                            else:
                                report["errors"].append(f"صف #{idx}: تاريخ المرتب غير مفهوم: {raw_date}")
                                continue
                year, month = sdate.year, sdate.month

                legacy = clean_value(row.get("legacy_code"))
                national_id = clean_value(row.get("national_id"))
                insurance_number = clean_value(row.get("insurance_number"))
                identifier = legacy or national_id or insurance_number or name
                key = (identifier, year, month)
                if key in seen:
                    report["errors"].append(f"صف #{idx}: تكرار لنفس الموظف ونفس الشهر ({identifier} - {year}-{month}) في الملف")
                    continue
                seen.add(key)

                # ابحث عن الموظف
                emp = None
                if legacy:
                    emp = self.session.exec(select(Employee).where(Employee.code == legacy)).first()
                if not emp and national_id:
                    emp = self.session.exec(select(Employee).where(Employee.national_id == national_id)).first()
                if not emp and insurance_number:
                    emp = self.session.exec(select(Employee).where(Employee.insurance_number == insurance_number)).first()
                if not emp:
                    # أنشئ موظف بسيط إن لزم
                    emp = Employee(full_name=name, tenant_id=self.tenant.id if hasattr(self.tenant, "id") else None)
                    self.session.add(emp)
                    self.session.flush()

                # تكرار في القاعدة
                exists = self.session.exec(
                    select(SalaryRecord).where(
                        SalaryRecord.employee_id == emp.id,
                        SalaryRecord.salary_year == year,
                        SalaryRecord.salary_month == month
                    )
                ).first()
                if exists:
                    report["warnings"].append(f"صف #{idx}: سجل مرتب موجود مسبقًا في القاعدة ({emp.id} - {year}-{month})")
                    continue

                # أرقام
                def to_num(v):
                    if v is None or (isinstance(v, str) and v.strip() == ""): return 0.0
                    if isinstance(v, (int, float)): return float(v)
                    s = re.sub(r"[^\d\.\-]", "", str(v).strip())
                    if s in ("", "."): return 0.0
                    try: return float(s)
                    except: return 0.0

                sal = SalaryRecord(
                    employee_id=emp.id,
                    salary_year=year,
                    salary_month=month,
                    base_salary=to_num(row.get("base_salary")),
                    allowances_food=to_num(row.get("allowances_food")),
                    allowances_travel=to_num(row.get("allowances_travel")),
                    allowances_transport=to_num(row.get("allowances_transport")),
                    allowances_other=to_num(row.get("allowances_other")),
                    deduction_insurance_employee=to_num(row.get("ded_insurance_employee")),
                    deduction_loans=to_num(row.get("ded_loans")),
                    net_salary=to_num(row.get("net_salary")),
                    attendance_days=int(to_num(row.get("attendance_days") or 0)),
                    absence_days=int(to_num(row.get("absence_days") or 0)),
                    payment_date=sdate,
                )
                self.session.add(sal)
                report["imported"] += 1

            if commit:
                self.session.commit()
                report["status"] = "success"
            else:
                self.session.rollback()
                report["status"] = "dry-run"

        except Exception as e:
            try: self.session.rollback()
            except: pass
            report["status"] = "failed"
            report["errors"].append(str(e))
        return report
