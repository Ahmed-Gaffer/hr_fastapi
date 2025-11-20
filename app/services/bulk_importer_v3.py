import re
import uuid
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

import openpyxl
from sqlmodel import Session, select

from app.models.employee import Employee
from app.models.site import Site
from app.models.cost_center import CostCenter
from app.models.salary_record import SalaryRecord
from app.models.salary_allowance import SalaryAllowance

NORMALIZE_MAP = {
    # مفاتيح شائعة -> مفتاح داخلي موحد
    "الكود القديم": "legacy_code",
    "كود الموظف": "legacy_code",
    "الاسم": "name",
    "موقع العمل": "site",
    "الادارة / المشروع": "cost_center",
    "الادارة / المشروع": "cost_center",
    "الوظيفة": "role",
    "تاريخ التأمين": "hire_date",
    "اساسي": "base_salary",
    "الأساسي": "base_salary",
    "اعاشة": "allowances_food",
    "سفر": "allowances_travel",
    "مواصلات": "allowances_transport",
    "بدلات اخري": "allowances_other",
    "تأمين اجتماعي (العامل)": "ded_insurance_employee",
    "أقساط": "ded_loans",
    "صافي الراتب المستحق": "net_salary",
    "الصافي": "net_salary",
    "مرتبات شهر": "salary_date",
    "تاريخ": "salary_date",
    "عدد أيام الحضور": "attendance_days",
    "عدد أيام الحضور": "attendance_days",
    "عدد ايام الغياب": "absence_days",
    "الرقم القومي": "national_id",
    "الرقم التأميني": "insurance_number",
    # أضف خرائط إضافية عند الحاجة
}

def norm_header(h: Optional[str]) -> Optional[str]:
    if not h:
        return None
    key = str(h).strip()
    return NORMALIZE_MAP.get(key, key)

def parse_num(v) -> float:
    if v is None or (isinstance(v, str) and v.strip() == ""):
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    # احذف أي أحرف غير الأرقام أو النقطة أو السالب
    cleaned = re.sub(r"[^\d\.\-]", "", s)
    if cleaned == "" or cleaned == ".":
        return 0.0
    try:
        return float(cleaned)
    except:
        return 0.0

class BulkImporterV3:
    """Importer tailored to your payroll sheet:
       - dry-run (no DB commit) or commit (save)
       - validates duplicates per employee-month
       - generates new code for new employees and returns mapping
    """
    def __init__(self, file_bytes: bytes, session: Session):
        self.wb = openpyxl.load_workbook(BytesIO(file_bytes), data_only=True)
        self.session = session
        self.report: Dict[str, Any] = {
            "sites": {"imported": 0, "errors": []},
            "cost_centers": {"imported": 0, "errors": []},
            "employees": {"created": 0, "updated": 0, "errors": []},
            "salaries": {"imported": 0, "errors": []},
            "warnings": [],
            "mapping_legacy_to_new": {},
            "status": "pending"
        }
        self._gen_counter = 0
        self._seen_salary_rows = set()  # (employee_identifier, year, month) to detect duplicates in file

    def _gen_code(self) -> str:
        self._gen_counter += 1
        ts = datetime.utcnow().strftime("%y%m%d%H%M%S")
        return f"EMP{ts}{self._gen_counter:03d}"

    def _find_or_create_site(self, name: Optional[str]):
        if not name:
            return None
        name = str(name).strip()
        s = self.session.exec(select(Site).where(Site.name == name)).first()
        if s:
            return s
        s = Site(name=name)
        self.session.add(s)
        self.session.flush()
        self.report["sites"]["imported"] += 1
        return s

    def _find_or_create_cost_center(self, name: Optional[str], site_obj: Optional[Site]):
        if not name:
            return None
        name = str(name).strip()
        cc = self.session.exec(select(CostCenter).where(CostCenter.name == name)).first()
        if cc:
            return cc
        cc = CostCenter(code=str(uuid.uuid4())[:8], name=name, site_id=(site_obj.id if site_obj else None))
        self.session.add(cc)
        self.session.flush()
        self.report["cost_centers"]["imported"] += 1
        return cc

    def _find_employee(self, legacy_code: Optional[str], national_id: Optional[str], insurance_number: Optional[str]) -> Optional[Employee]:
        q = None
        if legacy_code:
            q = self.session.exec(select(Employee).where(Employee.code == str(legacy_code).strip())).first()
            if q:
                return q
        if national_id:
            q = self.session.exec(select(Employee).where(Employee.national_id == str(national_id).strip())).first()
            if q:
                return q
        if insurance_number:
            q = self.session.exec(select(Employee).where(Employee.insurance_number == str(insurance_number).strip())).first()
            if q:
                return q
        return None

    def import_file(self, commit: bool = False) -> Dict[str, Any]:
        try:
            if "الرواتب" not in self.wb.sheetnames:
                self.report["salaries"]["errors"].append("شيت 'الرواتب' غير موجود")
                self.report["status"] = "failed"
                return self.report

            ws = self.wb["الرواتب"]
            headers = {}
            for idx, cell in enumerate(next(ws.iter_rows(min_row=1, max_row=1, values_only=True)), start=1):
                key = norm_header(cell)
                if key:
                    headers[key] = idx - 1  # 0-based

            required_keys = ["legacy_code", "name", "site", "cost_center", "role", "hire_date", "base_salary", "salary_date", "net_salary"]
            # proceed even if some optional missing; required at least legacy/name/salary_date/base/net
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                # تحويل الصف إلى dict بالـ headers المتعرف عليها
                rowd = {}
                for k, idx in headers.items():
                    rowd[k] = row[idx] if idx < len(row) else None

                # استخرج الحقول الأساسية
                legacy = rowd.get("legacy_code")
                name = rowd.get("name")
                if not name:
                    self.report["salaries"]["errors"].append(f"صف {row_idx}: الاسم مفقود")
                    continue

                salary_date_raw = rowd.get("salary_date")
                if not salary_date_raw:
                    self.report["salaries"]["errors"].append(f"صف {row_idx}: تاريخ المرتب (مرتبات شهر) مفقود")
                    continue
                # دعم التاريخ كـ Excel date أو نص
                if isinstance(salary_date_raw, datetime):
                    sdate = salary_date_raw.date()
                else:
                    try:
                        sdate = datetime.strptime(str(salary_date_raw).strip(), "%Y/%m/%d").date()
                    except:
                        try:
                            sdate = datetime.strptime(str(salary_date_raw).strip(), "%Y-%m-%d").date()
                        except:
                            # حاول استخراج السنة والشهر من نص "2025/10/01" أو "2025-10-01"
                            parts = re.findall(r"(\d{4})", str(salary_date_raw))
                            if parts:
                                y = int(parts[0])
                                m = 1
                                sdate = datetime(y, m, 1).date()
                            else:
                                self.report["salaries"]["errors"].append(f"صف {row_idx}: لم أستطع تحويل التاريخ '{salary_date_raw}'")
                                continue

                year, month = sdate.year, sdate.month

                # قيم عدد الحضور والغياب، الرواتب والبدلات والخصومات
                base_salary = parse_num(rowd.get("base_salary"))
                allowances_food = parse_num(rowd.get("allowances_food"))
                allowances_travel = parse_num(rowd.get("allowances_travel"))
                allowances_transport = parse_num(rowd.get("allowances_transport"))
                allowances_other = parse_num(rowd.get("allowances_other"))
                ded_insurance_employee = parse_num(rowd.get("ded_insurance_employee"))
                ded_loans = parse_num(rowd.get("ded_loans"))
                net_salary = parse_num(rowd.get("net_salary"))
                attendance_days = int(parse_num(rowd.get("attendance_days") or 0))
                absence_days = int(parse_num(rowd.get("absence_days") or 0))

                # تحقق من تكرار نفس الموظف لنفس الشهر داخل الملف
                identifier = (str(legacy).strip() if legacy else (str(rowd.get("national_id") or rowd.get("insurance_number") or name)).strip())
                seen_key = (identifier, year, month)
                if seen_key in self._seen_salary_rows:
                    self.report["salaries"]["errors"].append(f"صف {row_idx}: تكرار صف لذات الموظف ونفس الشهر ({identifier} - {year}-{month})")
                    continue
                self._seen_salary_rows.add(seen_key)

                # مواقع ومراكز تكلفة
                site_obj = self._find_or_create_site(rowd.get("site"))
                cc_obj = self._find_or_create_cost_center(rowd.get("cost_center"), site_obj)

                # ابحث عن الموظف في القاعدة أو أنشئ واحد جديد
                emp = self._find_employee(legacy, rowd.get("national_id"), rowd.get("insurance_number"))
                created_new = False
                if not emp:
                    new_code = self._gen_code()
                    emp = Employee(code=new_code, name=str(name).strip(), role=str(rowd.get("role") or "").strip(),
                                   site_id=(site_obj.id if site_obj else None),
                                   cost_center_id=(cc_obj.id if cc_obj else None),
                                   hire_date=(rowd.get("hire_date") if isinstance(rowd.get("hire_date"), datetime) else None))
                    # حاول تعيين الحقول الوطنية/تأمينية إن وجدت
                    try:
                        if rowd.get("national_id"):
                            emp.national_id = str(rowd.get("national_id")).strip()
                        if rowd.get("insurance_number"):
                            emp.insurance_number = str(rowd.get("insurance_number")).strip()
                        self.session.add(emp)
                        self.session.flush()
                        created_new = True
                        self.report["employees"]["created"] += 1
                        # سجل الماب (الكود القديم -> الجديد) لمرجعية
                        if legacy:
                            self.report["mapping_legacy_to_new"][str(legacy).strip()] = emp.code
                    except Exception as e:
                        self.report["employees"]["errors"].append(f"صف {row_idx}: خطأ أثناء إنشاء موظف جديد: {str(e)}")
                        continue
                else:
                    # حدث بيانات بسيطة إن لزم (موجود مسبقا)
                    emp_changed = False
                    if site_obj and emp.site_id != (site_obj.id if site_obj else None):
                        emp.site_id = site_obj.id
                        emp_changed = True
                    if cc_obj and emp.cost_center_id != (cc_obj.id if cc_obj else None):
                        emp.cost_center_id = cc_obj.id
                        emp_changed = True
                    if emp_changed:
                        try:
                            self.session.add(emp)
                            self.session.flush()
                            self.report["employees"]["updated"] += 1
                        except Exception as e:
                            self.report["employees"]["errors"].append(f"صف {row_idx}: خطأ أثناء تحديث الموظف: {str(e)}")
                            continue

                # تحقق من وجود سجل راتب لنفس الموظف ونفس الشهر في الـ DB
                exists_sal = self.session.exec(
                    select(SalaryRecord).where(
                        SalaryRecord.employee_id == emp.id,
                        SalaryRecord.salary_year == year,
                        SalaryRecord.salary_month == month
                    )
                ).first()
                if exists_sal:
                    self.report["salaries"]["errors"].append(f"صف {row_idx}: سجل مرتب موجود مسبقًا لنفس الموظف ونفس الشهر (DB) -> {emp.code} - {year}-{month}")
                    continue

                # أنشئ سجل الراتب
                try:
                    sal = SalaryRecord(
                        employee_id=emp.id,
                        salary_year=year,
                        salary_month=month,
                        base_salary=base_salary,
                        allowances_food=allowances_food,
                        allowances_travel=allowances_travel,
                        allowances_transport=allowances_transport,
                        allowances_other=allowances_other,
                        deduction_insurance_employee=ded_insurance_employee,
                        deduction_loans=ded_loans,
                        attendance_days=attendance_days,
                        absence_days=absence_days,
                        net_salary=net_salary,
                        payment_date=sdate
                    )
                    self.session.add(sal)
                    self.session.flush()
                    self.report["salaries"]["imported"] += 1
                except Exception as e:
                    self.report["salaries"]["errors"].append(f"صف {row_idx}: خطأ أثناء إضافة سجل الراتب: {str(e)}")
                    continue

            # نهاية الصفوف
            if commit:
                self.session.commit()
                self.report["status"] = "success"
            else:
                # dry-run => تراجع كل شيء
                self.session.rollback()
                self.report["status"] = "dry-run"
        except Exception as e:
            try:
                self.session.rollback()
            except:
                pass
            self.report["status"] = "failed"
            self.report["error"] = str(e)
        return self.report