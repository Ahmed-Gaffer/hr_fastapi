import tkinter as tk
from tkinter import filedialog
import os

def add_header_to_file(filepath):
    """إزالة التعليقات من أول الملف ثم إضافة هيدر جديد"""
    if not filepath.endswith((".py", ".rkt", ".txt", ".json", ".css")):
        return

    filename = os.path.basename(filepath)

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

    # إزالة التعليقات من بداية الملف فقط
    lines = content.splitlines()
    new_lines = []
    started = False
    for line in lines:
        if not started:
            if line.strip().startswith("#"):
                continue  # تجاهل التعليقات في البداية
            else:
                started = True
        new_lines.append(line)
    cleaned_content = "\n".join(new_lines)

    # إضافة الهيدر الجديد
    header = f"# File Path: {filepath}\n# File Name: {filename}\n# -----------------------------------------\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + cleaned_content)

def collect_files_from_folder(folder, extensions=None):
    filepaths = []
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if extensions:
                if any(file.endswith(ext) for ext in extensions):
                    filepaths.append(os.path.join(root_dir, file))
            else:
                filepaths.append(os.path.join(root_dir, file))
    return filepaths

# واجهة اختيار مجلدات متعددة (تكرار لحد ما المستخدم يضغط Cancel)
root = tk.Tk()
root.withdraw()

folders = []
while True:
    folder = filedialog.askdirectory(title="اختر مجلد رئيسي (اضغط Cancel للانتهاء)")
    if not folder:  # لو المستخدم ضغط Cancel
        break
    folders.append(folder)

extensions = [".py", ".rkt", ".txt", ".json", ".css"]

all_files = []
for folder in folders:
    all_files.extend(collect_files_from_folder(folder, extensions))

for path in all_files:
    add_header_to_file(path)

print("✅ تم مسح التعليقات القديمة من بداية الملفات وإضافة الهيدر الجديد")