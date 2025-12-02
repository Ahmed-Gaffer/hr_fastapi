import os

# المسارات اللي فيها الموديلات
LEVEL_DIRS = [
    "app/models",
    "app/models/levels/level1/employee_plus",
    "app/models/levels/level1/Intermediate",
    "app/models/levels/level1/units",
    "app/models/levels/level2",
    "app/models/levels/level3",
    "app/models/levels/level4",
]

IMPORTS = """from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
"""

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "SQLModel" in content and "from sqlmodel import SQLModel" not in content:
        print(f"🔄 إضافة الاستيرادات في: {file_path}")
        new_content = IMPORTS + "\n" + content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print(f"✅ لا يحتاج تعديل: {file_path}")

def process_directory(base_path):
    for filename in os.listdir(base_path):
        if filename.endswith(".py") and filename != "__init__.py":
            process_file(os.path.join(base_path, filename))

if __name__ == "__main__":
    for dir_path in LEVEL_DIRS:
        if os.path.exists(dir_path):
            process_directory(dir_path)
