# منطق حساب المرتبات بناءً على الحضور
from sqlmodel import Session, select
from app.database import engine
from app.models.attendance import Attendance
from app.models.salary import SalaryRecord

# دالة لحساب المرتب لموظف معين في شهر معين
def calculate_salary(employee_id: int, month: str, base_salary: float, deduction_per_day: float):
    with Session(engine) as session:
        # استخراج كل أيام الحضور للموظف في الشهر المحدد
        attendances = session.exec(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.date.startswith(month)
            )
        ).all()

        # حساب عدد أيام الحضور
        days_present = len(attendances)

        # حساب الخصومات
        deductions = 0
        # نفترض إن الشهر فيه 26 يوم عمل
        expected_days = 26
        if days_present < expected_days:
            deductions = (expected_days - days_present) * deduction_per_day

        # حساب المرتب النهائي
        net_salary = base_salary - deductions

        # إنشاء سجل المرتب
        salary = SalaryRecord(
            employee_id=employee_id,
            month=month,
            base_salary=base_salary,
            days_present=days_present,
            deductions=deductions,
            net_salary=net_salary
        )

        session.add(salary)
        session.commit()
        session.refresh(salary)
        return salary
