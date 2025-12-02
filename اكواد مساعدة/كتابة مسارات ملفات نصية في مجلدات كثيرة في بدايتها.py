import tkinter as tk
from tkinter import filedialog
import os

def add_header_to_file(filepath):
    """إضافة هيدر للملف إذا لم يكن موجود"""
    # تجاهل أي ملف مش بالامتدادات المطلوبة
    if not filepath.endswith((".py", ".rkt", ".txt", ".json", ".css")):
        return

    filename = os.path.basename(filepath)

    # محاولة قراءة الملف بترميزات مختلفة لتفادي مشاكل Unicode
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    content = None
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        print(f"⚠️ لم أستطع قراءة الملف: {filepath}")
        return

    if not content.startswith("# File Path:"):
        header = f"# File Path: {filepath}\n# File Name: {filename}\n# -----------------------------------------\n\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + content)

def collect_files_from_folder(folder, extensions=None):
    """
    جمع كل الملفات من مجلد رئيسي بما فيه المجلدات الفرعية.
    extensions: قائمة بالامتدادات المسموح بها (مثلاً ['.py', '.rkt'])
    لو None → يجمع كل الملفات.
    """
    filepaths = []
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if extensions:
                if any(file.endswith(ext) for ext in extensions):
                    filepaths.append(os.path.join(root_dir, file))
            else:
                filepaths.append(os.path.join(root_dir, file))
    return filepaths

# واجهة اختيار مجلدات متعددة
root = tk.Tk()
root.withdraw()

folders = []
while True:
    folder = filedialog.askdirectory(title="اختر مجلد رئيسي")
    if not folder:  # لو المستخدم ضغط Cancel
        break
    folders.append(folder)
    more = input("هل تريد إضافة مجلد آخر؟ (y/n): ")
    if more.lower() != "y":
        break

# هنا نحدد الامتدادات المطلوبة
extensions = [".py", ".rkt", ".txt", ".json", ".css"]

# جمع كل الملفات من المجلدات المختارة
all_files = []
for folder in folders:
    all_files.extend(collect_files_from_folder(folder, extensions))

# تحديث الملفات
for path in all_files:
    add_header_to_file(path)

print("✅ تم تحديث جميع الملفات المطلوبة داخل المجلدات المختارة بما فيها المجلدات الفرعية")