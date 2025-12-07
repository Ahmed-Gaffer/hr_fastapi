# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/tax_policy.py
# File Name: tax_policy.py
# -----------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
import json


class TaxPolicy(SQLModel, table=True):
    """سياسات ضريبية - شرائح متدرجة"""
    __tablename__ = "tax_policy"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 📌 بيانات السياسة
    name: str  # اسم السياسة (مثلاً: "ضريبة الدخل 2025")
    effective_from: date  # تاريخ بداية التطبيق
    effective_to: Optional[date] = None  # تاريخ نهاية التطبيق (لو مؤقتة)

    # 🔧 الشرائح (JSON للمرونة)
    brackets_json: str = Field(default="[]")

    notes: Optional[str] = None

    # 🛠️ دوال مساعدة لتحويل JSON إلى dict/list
    def get_brackets(self):
        return json.loads(self.brackets_json)

    def set_brackets(self, brackets):
        self.brackets_json = json.dumps(brackets)
