# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\services\tax_engine.py
# File Name: tax_engine.py
# -----------------------------------------

from datetime import date
from typing import List, Dict, Optional
from sqlmodel import Session, select
from app.models.tax_policy import TaxPolicy

def calculate_progressive_tax(amount: float, brackets: List[Dict]) -> float:
    """حساب ضريبة تصاعدية بناءً على الشرائح"""
    if amount <= 0:
        return 0.0
    
    remaining = amount
    prev_limit = 0.0
    tax = 0.0
    
    for br in brackets:
        upto = br.get("upto")
        rate = float(br.get("rate", 0.0))
        
        if upto is None:
            portion = max(0.0, amount - prev_limit)
            tax += portion * rate
            break
        
        limit = float(upto)
        if amount > prev_limit:
            portion = max(0.0, min(amount, limit) - prev_limit)
            tax += portion * rate
            prev_limit = limit
    
    return round(tax, 2)

def get_policy_for_date(session: Session, target_date: date) -> Optional[TaxPolicy]:
    """احصل على السياسة الضريبية للتاريخ المحدد"""
    q = session.exec(
        select(TaxPolicy)
        .where(TaxPolicy.effective_from <= target_date)
        .order_by(TaxPolicy.effective_from.desc())
    ).all()
    
    for p in q:
        if (p.effective_to is None) or (target_date <= p.effective_to):
            return p
    return None

def compute_tax_for_date(session: Session, taxable_amount: float, target_date: date) -> float:
    """احسب الضريبة للتاريخ المحدد باستخدام السياسة المناسبة"""
    policy = get_policy_for_date(session, target_date)
    if not policy:
        return 0.0
    brackets = policy.get_brackets()
    return calculate_progressive_tax(taxable_amount, brackets)