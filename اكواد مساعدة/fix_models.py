import re
import argparse
import shutil
from pathlib import Path

# =============== أدوات مساعدة ===============

def to_camel(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name)
    return "".join(p.capitalize() for p in parts if p)

def safe_read(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def safe_write(path: Path, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def backup_file(src: Path, backup_dir: Path):
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, backup_dir / src.name)

def detect_classes_with_bases(content: str):
    # يرجّع [(class_name, bases_text, body_text)]
    pattern = r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\):\s*\n(.*?)(?=\nclass\s+|\Z)"
    return re.findall(pattern, content, flags=re.S)

def fix_class_name_in_content(content: str, old_name: str, new_name: str) -> str:
    text = content
    # تعريف الكلاس
    text = re.sub(rf"(class\s+){old_name}(\s*\()", rf"\1{new_name}\2", text)
    # الإشارات العامة الآمنة (كلمات مستقلة)
    text = re.sub(rf"\b{old_name}\b", new_name, text)
    return text

def count_required_fields(body: str) -> int:
    # يعتبر الحقل إلزامي إذا لم يحتوي على Optional أو Default
    required = 0
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # محاولة بسيطة لاكتشاف التعريفات من نمط SQLModel/typing
        if ":" in line:
            # مثال: name: str = "x"
            has_optional = "Optional[" in line or "Optional[".lower() in line.lower()
            has_default = "=" in line
            if not has_optional and not has_default:
                required += 1
    return required

def is_table_model(bases_text: str, body_text: str) -> bool:
    # نحاول اكتشاف table=True داخل تعريف SQLModel
    # ليس دقيق 100% لكنه يكفي للاستخدام الحالي
    if "table=True" in bases_text:
        return True
    # أحيانًا يكون table=True داخل السطر الأول بعد التعريف
    first_line = body_text.splitlines()[0].strip() if body_text.splitlines() else ""
    return "table=True" in first_line

def classify_name(file_stem: str, cls_name: str, bases_text: str, body_text: str) -> str:
    base = to_camel(file_stem)

    # 1) Enum → Status/Category حسب السياق، الافتراضي Status
    if "Enum" in bases_text:
        # لو اسم الملف يحتوي على كلمات معينة
        lower_stem = file_stem.lower()
        if "category" in lower_stem:
            return base + "Category"
        return base + "Status"

    # 2) الموديل الرئيسي (table=True) → اسم الملف نفسه
    if is_table_model(bases_text, body_text):
        return base

    # 3) موديلات الإدخال/التحديث (بدون table=True)
    # - لو فيه حقول إلزامية أكثر → Create
    # - لو معظم الحقول اختيارية → Update
    required = count_required_fields(body_text)
    # بسيط: لو فيه 2+ حقول إلزامية نعتبره Create، وإلا Update
    if required >= 2:
        return base + "Create"
    else:
        return base + "Update"

def normalize_init_import_line(line: str, file_classes: list[str]) -> str:
    # يضبط أسماء الموديلات في الاستيراد لتطابق الأسماء بعد الإصلاح
    m = re.match(r"from\s+(\.?.+)\s+import\s+(.+)", line.strip())
    if not m:
        return line
    module_path, names = m.groups()
    fixed_names = []
    for n in [x.strip() for x in names.split(",")]:
        # لو الاسم موجود بالـ case المختلف، نختار النسخة المصححة
        matches = [c for c in file_classes if c.lower() == n.lower()]
        if matches:
            fixed_names.append(matches[0])
        else:
            # محاولة تحويله لاسم Camel مناسب
            fixed_names.append(to_camel(n))
    return f"from {module_path} import {', '.join(fixed_names)}"

# =============== المنطق الرئيسي ===============

def main(base_path: str, dry_run: bool, apply: bool):
    base = Path(base_path)
    init_path = base / "__init__.py"
    backup_dir = base / "_backup_models"
    backup_dir.mkdir(exist_ok=True)

    report = []
    file_class_map = {}  # {filename: [final_class_names]}

    # 1) إصلاح أسماء الكلاسات داخل كل الملفات
    for file_py in base.glob("*.py"):
        if file_py.name == "__init__.py":
            continue
        content = safe_read(file_py)
        class_defs = detect_classes_with_bases(content)
        changes = []
        for cls_name, bases_text, body_text in class_defs:
            new_name = classify_name(file_py.stem, cls_name, bases_text, body_text)
            if new_name != cls_name:
                changes.append((cls_name, new_name))

        # تطبيق التغييرات داخل الملف
        if changes:
            report.append(f"📄 {file_py.name}: {len(changes)} تعديل")
            for old, new in changes:
                report.append(f"   🔧 {old} -> {new}")
            if apply:
                backup_file(file_py, backup_dir)
                new_content = content
                for old, new in changes:
                    new_content = fix_class_name_in_content(new_content, old, new)
                safe_write(file_py, new_content)
                # حدّث قائمة الكلاسات النهائية لهذا الملف
                final_defs = detect_classes_with_bases(new_content)
                file_class_map[file_py.name] = [c[0] for c in final_defs]
            else:
                # لو dry-run، نبني الماب من المحتوى الأصلي مع توقع التغيير
                predicted = []
                for cls_name, _, _ in class_defs:
                    nn = next((n for o, n in changes if o == cls_name), cls_name)
                    predicted.append(nn)
                file_class_map[file_py.name] = predicted
        else:
            # لا تغييرات: نسجّل الأسماء الحالية
            file_class_map[file_py.name] = [c[0] for c in class_defs]

    # 2) إصلاح الاستيرادات في __init__.py بناءً على الأسماء النهائية
    if init_path.exists():
        init_content = safe_read(init_path)
        import_lines = [
            ln for ln in init_content.splitlines()
            if ln.strip().startswith("from ") and " import " in ln and not ln.strip().startswith("#")
        ]
        changes_init = []
        for line in import_lines:
            m = re.match(r"from\s+(\.?.+)\s+import\s+(.+)", line.strip())
            if not m:
                continue
            module_path, _ = m.groups()
            # تحديد اسم الملف الهدف
            target_file = module_path.replace(".", "/") + ".py"
            target_name = Path(target_file).name
            # لو الملف موجود في الماب، نطبع ونعدل
            if target_name in file_class_map:
                fixed_line = normalize_init_import_line(line, file_class_map[target_name])
                if fixed_line != line:
                    changes_init.append((line, fixed_line))

        # تطبيق تغييرات __init__.py
        if changes_init:
            report.append(f"📝 تعديل __init__.py: {len(changes_init)} سطر")
            for old, new in changes_init:
                report.append(f"   - {old.strip()} -> {new.strip()}")
            if apply:
                backup_file(init_path, backup_dir)
                new_init = init_content
                for old_line, new_line in changes_init:
                    new_init = new_init.replace(old_line, new_line)
                safe_write(init_path, new_init)

    # 3) طباعة التقرير
    print("\n===== تقرير الفحص والإصلاح =====")
    for r in report:
        print(r)

    if apply:
        print("\n✅ تم التطبيق بنجاح. نُسخ احتياطيًا في:", backup_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart fixer for class names and __init__ imports in models.")
    parser.add_argument("--path", required=True, help="مسار مجلد app/models")
    parser.add_argument("--dry-run", action="store_true", help="فحص بدون تعديل")
    parser.add_argument("--apply", action="store_true", help="تطبيق الإصلاحات مع نسخة احتياطية")
    args = parser.parse_args()
    main(args.path, args.dry_run, args.apply)
