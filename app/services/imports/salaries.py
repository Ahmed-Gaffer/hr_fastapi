# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\imports\salaries.py
# File Name: salaries.py
# -----------------------------------------



# app/services/imports/salaries.py
import pandas as pd
import re
from sqlmodel import Session, select
from datetime import datetime
from app.models.employee import Employee
from app.models.salary import Salary
from app.services.helpers import clean_value, parse_date
from app.services.headers import SALARY_hEADERS
from app.services.imports.base_importer import BaseImporter
from app.services.cleaners import clean_salary_data
from datetime import date

class SalaryImporter(BaseImporter):
    def run(self, session: Session, tenant, stream, commit: bool = True, allow_create_employee: bool = True):
        file_id = f"sal-{int(datetime.utcnow().timestamp())}"
        report = self.new_report(file_id, not commit)

        try:
            # قراءة + تنظيف
            df = clean_salary_data(stream)
            df.rename(columns={k: v for k, v in SALARY_hEADERS.items() if k in df.columns}, inplace=True)

            seen = set()
            for idx, row in df.iterrows():
                name = clean_value(row.get("name"))
                salary_date = row.get("salary_date") or row.get("month") or row.get("date")
                sdate = parse_date(salary_date)
                if not sdate:
                    month_value = clean_value(row.get("month")) or clean_value(row.get("salary_month"))
                    year_value = clean_value(row.get("year")) or clean_value(row.get("salary_year"))
                    if month_value:
                        try:
                            month_num = int(str(month_value).strip().split()[0])
                            year_num = int(str(year_value).strip()) if year_value else datetime.utcnow().year
                            sdate = date(year_num, month_num, 1)
                        except Exception:
                            sdate = None
                if not name or not sdate:
                    report["rejected"] += 1
                    report["errors"].append(f"صف #{idx}: الاسم أو التاريخ غير صالح")
                    continue

                year, month = sdate.year, sdate.month
                legacy = clean_value(row.get("legacy_code"))
                nid = clean_value(row.get("national_id"))
                insurance = clean_value(row.get("insurance_number"))

                identifier = legacy or nid or insurance or name
                key = (identifier, year, month)
                if key in seen:
                    report["rejected"] += 1
                    report["warnings"].append(f"صف #{idx}: تكرار لنفس الموظف والشهر")
                    continue
                seen.add(key)

                emp = None
                if legacy:
                    emp = session.exec(select(Employee).where(Employee.legacy_code == legacy)).first()
                if not emp and nid:
                    emp = session.exec(select(Employee).where(Employee.national_id == nid)).first()
                if not emp and insurance:
                    emp = session.exec(select(Employee).where(Employee.insurance_number == insurance)).first()

                if not emp:
                    if allow_create_employee:
                        employee_code = legacy or nid or insurance or f"import-{idx}"
                        emp = Employee(name=name, code=employee_code, tenant_id=getattr(tenant, "id", None))
                        session.add(emp); session.flush()
                        report["added"] += 1
                    else:
                        report["rejected"] += 1
                        report["warnings"].append(f"صف #{idx}: الموظف غير موجود")
                        continue
                else:
                    report["updated"] += 1

                def to_num(v):
                    if v is None: return 0.0
                    s = re.sub(r"[^\d\.\-]", "", str(v).strip())
                    return float(s) if s else 0.0

                exists = session.exec(
                    select(Salary).where(
                        (Salary.employee_id == emp.id) &
                        (Salary.salary_year == year) &
                        (Salary.salary_month == month)
                    )
                ).first()
                if exists:
                    report["rejected"] += 1
                    report["warnings"].append(f"صف #{idx}: سجل مرتب موجود مسبقًا")
                    continue

                sal = Salary(
                    employee_id=emp.id,
                    salary_year=year,
                    salary_month=month,
                    base_salary=to_num(row.get("base_salary")),
                    net_salary=to_num(row.get("net_salary")),
                    payment_date=sdate
                )
                session.add(sal)
                report["added"] += 1

            if commit:
                session.commit(); report["status"] = "success"
            else:
                self.safe_rollback(session); report["status"] = "dry-run"

        except Exception as e:
            self.safe_rollback(session)
            report["status"] = "failed"; report["errors"].append(str(e))

        return self.finalize_report(report)