# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\scripts\import_employees.py
# File Name: import_employees.py
# -----------------------------------------

# سكريبت خارجي لتشغيل استيراد الموظفين من ملف Excel

# استيراد الدالة الخاصة بالاستيراد من ملف الخدمات
from app.services.import_excel import import_employees_from_excel

# تحديد مسار ملف Excel اللي فيه بيانات الموظفين
excel_path = "employees.xlsx"

# استدعاء الدالة مع تمرير المسار
import_employees_from_excel(excel_path)
