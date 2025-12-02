import os
import ast

# المسار لمجلد employee_plus
base_path = "app/models/levels/level1/employee_plus"

for filename in os.listdir(base_path):
    if filename.endswith(".py"):
        file_path = os.path.join(base_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        try:
            tree = ast.parse(source)
            classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
            print(f"{filename}: {classes}")
        except Exception as e:
            print(f"{filename}: Error parsing ({e})")
