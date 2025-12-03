from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
import json

class TaxPolicy(SQLModel, table=True):
    """سياسات ضريبية - شرائح متدرجة"""
    id: Optional[int] = Field(default=None, primary_key=True)

    # 📌 بيانات السياسة
    name: str  # اسم السياسة (مثلاً: "ضريبة الدخل 2025")
    effective_from: date  # تاريخ بداية التطبيق
    effective_to: Optional[date] = None  # تاريخ نهاية التطبيق

    brackets_json: str = Field(default="[]")  # الشرائح الضريبية بصيغة JSON
    notes: Optional[str] = None

    # 🛠️ دوال مساعدة
    def get_brackets(self):
        return json.loads(self.brackets_json)

    def set_brackets(self, brackets):
        self.brackets_json = json.dumps(brackets, ensure_ascii=False)
