from sqlmodel import Session, select
from app.models.salary_record import SalaryRecord
from app.models.benefit_record import BenefitRecord, BenefitType

class BenefitCalculator:
    """حساب البدلات (عينية ونقدية)"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def separate_benefits(self, salary_record_id: int) -> dict:
        """فصل البدلات العينية عن النقدية"""
        
        salary = self.session.exec(
            select(SalaryRecord).where(SalaryRecord.id == salary_record_id)
        ).first()
        
        if not salary:
            raise Exception(f"سجل راتب {salary_record_id} غير موجود")
        
        # البدلات العينية (تُضاف ثم تُخصم)
        in_kind_benefits = {
            "meals": salary.allowance_food,
            "transport": salary.allowance_transport,
            "travel": salary.allowance_travel,
        }
        
        total_in_kind = sum(in_kind_benefits.values())
        
        # البدلات النقدية (تُضاف ولا تُخصم)
        cash_benefits = salary.allowance_position  # بدلات أخرى نقدية
        
        return {
            "in_kind": {
                "meals": round(in_kind_benefits["meals"], 2),
                "transport": round(in_kind_benefits["transport"], 2),
                "travel": round(in_kind_benefits["travel"], 2),
                "total": round(total_in_kind, 2),
                "will_be_deducted": True  # سيتم خصمها لاحقاً
            },
            "cash": {
                "allowances": round(cash_benefits, 2),
                "will_be_deducted": False  # لن يتم خصمها
            }
        }