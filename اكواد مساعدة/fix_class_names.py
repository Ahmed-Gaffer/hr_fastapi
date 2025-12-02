import os
import ast

# المسارات اللي عايزين نراجعها
LEVEL_DIRS = [
    "app/models/levels/level1/employee_plus",
    "app/models/levels/level1/Intermediate",
    "app/models/levels/level1/units",
    "app/models/levels/level2",
    "app/models/levels/level3",
    "app/models/levels/level4",
]

def fix_class_name_from_filename(filename: str) -> str:
    """حوّل اسم الملف إلى اسم كلاس بنفس الشكل مع الحفاظ على الـ Case"""
    name = filename.replace(".py", "")
    parts = name.split("_")
    return "_".join([p[0].upper() + p[1:] if p else "" for p in parts])

def process_directory(base_path: str):
    print(f"\n📂 مراجعة المجلد: {base_path}")
    for filename in os.listdir(base_path):
        if filename.endswith(".py"):
            file_path = os.path.join(base_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            try:
                tree = ast.parse(source)
                classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
                if not classes:
                    continue

                expected_class_name = fix_class_name_from_filename(filename)
                current_class_name = classes[0].name

                if current_class_name != expected_class_name:
                    print(f"🔄 تعديل: {filename} => {current_class_name} → {expected_class_name}")
                    new_source = source.replace(f"class {current_class_name}", f"class {expected_class_name}")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_source)
                else:
                    print(f"✅ مطابق: {filename} => {current_class_name}")

            except Exception as e:
                print(f"⚠️ خطأ في {filename}: {e}")

if __name__ == "__main__":
    for dir_path in LEVEL_DIRS:
        if os.path.exists(dir_path):
            process_directory(dir_path)
        else:
            print(f"⚠️ المجلد غير موجود: {dir_path}")
