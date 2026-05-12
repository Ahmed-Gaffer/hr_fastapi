# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\scripts\import_employees.py
# File Name: import_employees.py
# -----------------------------------------

# سكريبت خارجي لتشغيل استيراد الموظفين من ملف Excel

# استيراد الدالة الخاصة بالاستيراد من ملف الخدمات
from app.services.import_excel import import_employees_from_excel

import sys
from pathlib import Path

# تحديد ملف Excel من الوسيطات أو استخدام الملف الافتراضي
excel_files = sys.argv[1:] or ["data/embloyees .1.xlsx"]
for excel_path in excel_files:
    print(f"استيراد الملف: {excel_path}")
    result = import_employees_from_excel(excel_path)
    print(result)
