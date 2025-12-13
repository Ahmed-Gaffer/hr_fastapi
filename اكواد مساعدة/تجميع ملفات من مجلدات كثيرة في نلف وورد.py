import tkinter as tk
from tkinter import filedialog
import os
from docx import Document
import re

# الامتدادات المطلوبة
TARGET_EXTENSIONS = [".py", ".rkt", ".txt", ".json", ".css"]

def clean_text(text):
    """تنظيف النص من الرموز غير الصالحة للـ XML"""
    text = text.replace("\x00", "")
    text = re.sub(r"[\x01-\x08\x0B-\x0C\x0E-\x1F]", "", text)
    return text

def collect_files_from_folder(folder, extensions):
    """جمع كل الملفات من مجلد رئيسي بما فيه المجلدات الفرعية"""
    filepaths = []
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepaths.append(os.path.join(root_dir, file))
    return filepaths

def read_file_content(filepath):
    """قراءة محتوى الملف مع محاولة أكثر من ترميز"""
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return None

def main():
    root = tk.Tk()
    root.withdraw()

    # اختيار ملفات متعددة دفعة واحدة (Ctrl/Shift)
    files = filedialog.askopenfilenames(
        title="اختر ملفات مباشرة (يمكنك استخدام Ctrl/Shift)",
        filetypes=[("Text/Code files", "*.py *.rkt *.txt *.json *.css"), ("All files", "*.*")]
    )

    # اختيار مجلدات متعددة (واحد واحد لحد ما تضغط Cancel)
    folders = []
    while True:
        folder = filedialog.askdirectory(title="اختر مجلد رئيسي (اضغط Cancel للانتهاء)")
        if not folder:
            break
        folders.append(folder)

    # لو ما اخترتش أي حاجة
    if not files and not folders:
        print("❌ لم يتم اختيار أي ملف أو مجلد")
        return

    # جمع كل الملفات من الملفات والمجلدات
    all_files = list(files)
    for folder in folders:
        all_files.extend(collect_files_from_folder(folder, TARGET_EXTENSIONS))

    # إنشاء ملف Word جديد
    doc = Document()
    doc.add_heading("تجميع محتويات الملفات", level=0)

    for path in all_files:
        if not path.endswith(tuple(TARGET_EXTENSIONS)):
            continue
        content = read_file_content(path)
        if content:
            content = clean_text(content)
            doc.add_heading(f"ملف: {path}", level=1)
            doc.add_paragraph(content)
            doc.add_page_break()  # فاصل بين كل ملف
        else:
            doc.add_heading(f"⚠️ لم أستطع قراءة الملف: {path}", level=2)

    # حفظ الملف النهائي
    output_path = os.path.join(os.getcwd(), "merged_files.docx")
    doc.save(output_path)
    print(f"✅ تم حفظ كل الملفات والمجلدات بمحتواها في: {output_path}")

if __name__ == "__main__":
    main()