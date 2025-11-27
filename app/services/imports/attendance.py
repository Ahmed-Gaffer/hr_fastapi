# app/services/imports/attendance.py
import pandas as pd
from sqlmodel import Session, select
from datetime import datetime
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.services.helpers import clean_value, parse_date
from app.services.headers import ATTENDANCE_HEADERS
from app.services.imports.base_importer import BaseImporter
from app.services.cleaners import clean_attendance_data  # ← إضافة

class AttendanceImporter(BaseImporter):
    def run(self, session: Session, tenant, stream, commit: bool = True):
        file_id = f"att-{int(datetime.utcnow().timestamp())}"
        report = self.new_report(file_id, not commit)

        try:
            # قراءة + تنظيف
            df = clean_attendance_data(stream)
            # توحيد أسماء الأعمدة حسب الهيدر المخصص
            df.rename(columns={k: v for k, v in ATTENDANCE_HEADERS.items() if k in df.columns}, inplace=True)

            seen = set()
            for idx, row in df.iterrows():
                name = clean_value(row.get("name"))
                sdate = parse_date(row.get("date"))

                if not name or not sdate:
                    report["rejected"] += 1
                    report["errors"].append(f"صف #{idx}: الاسم أو التاريخ غير صالح")
                    continue

                nid = clean_value(row.get("national_id"))
                legacy = clean_value(row.get("legacy_code"))
                identifier = nid or legacy or name
                key = (identifier, sdate)
                if key in seen:
                    report["rejected"] += 1
                    report["warnings"].append(f"صف #{idx}: تكرار لنفس الموظف في نفس اليوم")
                    continue
                seen.add(key)

                emp = None
                if nid:
                    emp = session.exec(select(Employee).where(Employee.national_id == nid)).first()
                if not emp and legacy:
                    emp = session.exec(select(Employee).where(Employee.legacy_code == legacy)).first()
                if not emp:
                    report["rejected"] += 1
                    report["warnings"].append(f"صف #{idx}: الموظف غير موجود")
                    continue

                exists = session.exec(
                    select(Attendance).where(
                        (Attendance.employee_id == emp.id) & (Attendance.date == sdate)
                    )
                ).first()
                if exists:
                    report["rejected"] += 1
                    report["warnings"].append(f"صف #{idx}: سجل حضور موجود مسبقًا")
                    continue

                att = Attendance(
                    employee_id=emp.id,
                    date=sdate,
                    status=clean_value(row.get("status")),
                    shift=clean_value(row.get("shift"))
                )
                session.add(att)
                report["added"] += 1

            if commit:
                session.commit(); report["status"] = "success"
            else:
                self.safe_rollback(session); report["status"] = "dry-run"

        except Exception as e:
            self.safe_rollback(session)
            report["status"] = "failed"; report["errors"].append(str(e))

        return self.finalize_report(report)
