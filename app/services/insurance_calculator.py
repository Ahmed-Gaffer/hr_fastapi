# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\insurance_calculator.py
# File Name: insurance_calculator.py
# -----------------------------------------



from sqlmodel import Session, select
from app.models.employee import Employee
from app.models.employee_details import EmployeeDetails

COMPREHENSIVE_iNSURANCE_gOVERNORATES = {
    "الأقصر", "بورسعيد", "الإسماعيلية", "السويس", "البحر الأحمر",
    "مطروح", "أسوان", "الإسكندرية", "البحيرة", "دمياط", "سوهاج",
    "شمال سيناء", "جنوب سيناء", "قنا", "كفر الشيخ"
}

class InsuranceCalculator:
    """حساب التأمينات (اجتماعي وصحي شامل)"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def calculate_employee_insurance(self, employee_id: int, basic_salary: float) -> dict:
        """حساب حصة العامل من التأمينات"""
        
        emp = self.session.exec(
            select(Employee).where(Employee.id == employee_id)
        ).first()
        
        details = self.session.exec(
            select(EmployeeDetails).where(EmployeeDetails.employee_id == employee_id)
        ).first()
        
        if not details:
            # قيم افتراضية
            details = EmployeeDetails(
                employee_id=employee_id,
                marital_status="أعزب",
                spouse_works=False,
                num_children=0,
                governorate="القاهرة"
            )
        
        # 1️⃣ التأمين الاجتماعي (10% ثابت)
        social_insurance = basic_salary * 0.10
        
        # 2️⃣ التأمين الصحي الشامل (متغير)
        health_insurance = 0.0
        
        # موظف لوحده: 1%
        health_insurance = basic_salary * 0.01
        
        # أطفال: 1% لكل طفل
        if details.num_children > 0:
            health_insurance += basic_salary * (0.01 * details.num_children)
        
        # زوجة: 3% إن لم تعمل، 0% إن كانت تعمل
        if details.marital_status == "متزوج":
            if not details.spouse_works:
                health_insurance += basic_salary * 0.03
        
        total_employee_insurance = social_insurance + health_insurance
        
        return {
            "social_insurance": round(social_insurance, 2),
            "health_insurance": round(health_insurance, 2),
            "total": round(total_employee_insurance, 2),
            "breakdown": {
                "employee_self": basic_salary * 0.01,
                "children": basic_salary * (0.01 * details.num_children) if details.num_children > 0 else 0,
                "spouse": basic_salary * 0.03 if (details.marital_status == "متزوج" and not details.spouse_works) else 0
            }
        }
    
    def calculate_employer_insurance(self, employee_id: int, basic_salary: float) -> dict:
        """حساب حصة صاحب العمل من التأمينات"""
        
        details = self.session.exec(
            select(EmployeeDetails).where(EmployeeDetails.employee_id == employee_id)
        ).first()
        
        if not details:
            details = EmployeeDetails(
                employee_id=employee_id,
                governorate="القاهرة"
            )
        
        # 1️⃣ التأمين الاجتماعي (14.75% ثابت)
        social_insurance = basic_salary * 0.1475
        
        # 2️⃣ التأمين الصحي الشامل (4% إن كان في محافظة مشمولة)
        health_insurance = 0.0
        if details.governorate in COMPREHENSIVE_iNSURANCE_gOVERNORATES:
            health_insurance = basic_salary * 0.04
        
        total_employer_insurance = social_insurance + health_insurance
        
        return {
            "social_insurance": round(social_insurance, 2),
            "health_insurance": round(health_insurance, 2),
            "total": round(total_employer_insurance, 2),
            "details": {
                "governorate": details.governorate,
                "has_comprehensive": details.governorate in COMPREHENSIVE_iNSURANCE_gOVERNORATES
            }
        }