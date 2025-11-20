# استخدم هذا المثال في سكربت إدخال (manual import)
# filepath: e:\خاص احمد جعفر\برمجة\مشاريع\hr_fastapi\scripts\create_tax_policy_example.py
from datetime import date
from sqlmodel import Session
from app.database import get_session
from app.models.tax_policy import TaxPolicy

brackets = [
    {"upto": 40000, "rate": 0.0},
    {"upto": 55000, "rate": 0.10},
    {"upto": 70000, "rate": 0.15},
    {"upto": 200000, "rate": 0.20},
    {"upto": 400000, "rate": 0.225},
    {"upto": 600000, "rate": 0.25},
    {"upto": 700000, "rate": 0.25},
    {"upto": 800000, "rate": 0.25},
    {"upto": 900000, "rate": 0.25},
    {"upto": 1200000, "rate": 0.25},
    {"upto": None, "rate": 0.275}
]

with get_session() as session:
    p = TaxPolicy(name="legacy_policy_complex", effective_from=date(2021,1,1))
    p.set_brackets(brackets)
    session.add(p)
    session.commit()
    print("created policy", p.id)