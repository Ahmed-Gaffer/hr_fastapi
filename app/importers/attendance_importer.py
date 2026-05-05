import pandas as pd
from sqlmodel import Session, select
from datetime import datetime
from app.models.employee import Employee
from app.models.attendance import Attendance


class AttendanceImporter:

    def run(self, session: Session, tenant_id: int, df: pd.DataFrame):
        added = 0
        rejected = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                employee_code = str(row.get("employee_code")).strip()
                date = row.get("date")

                if not employee_code or not date:
                    rejected += 1
                    continue

                employee = session.exec(
                    select(Employee).where(
                        Employee.code == employee_code,
                        Employee.tenant_id == tenant_id
                    )
                ).first()

                if not employee:
                    rejected += 1
                    continue

                exists = session.exec(
                    select(Attendance).where(
                        Attendance.employee_id == employee.id,
                        Attendance.date == date
                    )
                ).first()

                if exists:
                    rejected += 1
                    continue

                attendance = Attendance(
                    tenant_id=tenant_id,
                    employee_id=employee.id,
                    date=date,
                    status=row.get("status") or "present",
                    shift=row.get("shift"),
                    created_at=datetime.utcnow()
                )

                session.add(attendance)
                added += 1

            except Exception as e:
                rejected += 1
                errors.append(str(e))

        session.commit()

        return {
            "added": added,
            "rejected": rejected,
            "errors": errors
        }
