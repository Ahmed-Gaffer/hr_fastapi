from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
import json

class TaxPolicy(SQLModel, table=True):
    """سياسات ضريبية - شرائح متدرجة"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    effective_from: date
    effective_to: Optional[date] = None
    brackets_json: str = Field(default="[]")
    notes: Optional[str] = None

    def get_brackets(self):
        return json.loads(self.brackets_json)

    def set_brackets(self, brackets):
        self.brackets_json = json.dumps(brackets)