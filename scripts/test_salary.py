# سكريبت لحساب مرتب موظف معين في شهر معين

from app.services.salary_logic import calculate_salary

# استدعاء الدالة مع البيانات المطلوبة
salary = calculate_salary(
    employee_id=1,              # رقم الموظف
    month="2025-11",            # الشهر
    base_salary=5000.0,         # المرتب الأساسي
    deduction_per_day=100.0     # الخصم عن كل يوم غياب
)

# طباعة النتيجة
print("تم حساب المرتب:")
print(salary)
