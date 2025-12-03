import os
import re

# المسار الأساسي للموديلات
BASE_DIR = r"E:\خاص احمد جعفر\برمجة\مشاريع\hr_fastapi\app\models"

# النمط الاحترافي: CamelCase للكلاسات
camel_case_pattern = re.compile(r"class\s+([A-Z][a-zA-Z0-9]+)\s*\(")

report = []

def check_file(file_path):
    issues = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        # استخراج أسماء الكلاسات
        classes = camel_case_pattern.findall(content)

        if not classes:
            issues.append("❌ لا يوجد كلاس معرف في الملف")

        # لو فيه كلاس باسم مش CamelCase (مثلاً Employee_CostCenter)
        bad_names = re.findall(r"class\s+([A-Za-z0-9_]+)\s*\(", content)
        for name in bad_names:
            if "_" in name:
                issues.append(f"⚠️ الكلاس '{name}' مش CamelCase (مفروض يتكتب مثلاً EmployeeCostCenter)")

        # التحقق من وجود موديلات Create/Update
        if "Create" not in content and "Update" not in content:
            issues.append("⚠️ لا يوجد موديلات Create/Update في الملف")

    return issues


# المرور على كل الملفات داخل models
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            path = os.path.join(root, file)
            issues = check_file(path)
            if issues:
                report.append(f"\n📂 ملف: {path}")
                report.extend(issues)

# كتابة التقرير في ملف خارجي
report_path = "models_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"✅ تم إنشاء التقرير في: {report_path}")
