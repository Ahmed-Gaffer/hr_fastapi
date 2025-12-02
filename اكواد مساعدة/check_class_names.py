import os
import ast

# المجلدات اللي عايزين نراجعها
LEVEL_DIRS = [
    "app/models/levels/level1/employee_plus",
    "app/models/levels/level1/Intermediate",
    "app/models/levels/level1/units",
    "app/models/levels/level2",
    "app/models/levels/level3",
    "app/models/levels/level4",
]

def check_classes_in_file(file_path, filename):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source)
        classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
        if classes:
            print(f"{filename}: {classes}")
        else:
            print(f"{filename}: ❌ مفيش كلاس")
    except Exception as e:
        print(f"{filename}: ⚠️ خطأ في قراءة الملف ({e})")

def process_directory(base_path):
    print(f"\n📂 مراجعة المجلد: {base_path}")
    for filename in os.listdir(base_path):
        if filename.endswith(".py"):
            file_path = os.path.join(base_path, filename)
            check_classes_in_file(file_path, filename)

if __name__ == "__main__":
    for dir_path in LEVEL_DIRS:
        if os.path.exists(dir_path):
            process_directory(dir_path)
        else:
            print(f"⚠️ المجلد غير موجود: {dir_path}")
