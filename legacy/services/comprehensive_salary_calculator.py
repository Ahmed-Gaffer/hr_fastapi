# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\comprehensive_salary_calculator.py
# File Name: comprehensive_salary_calculator.py
# -----------------------------------------



from datetime import datetime, date
from sqlmodel import Session, select
from app.models.employee import Employee
from app.models.salary import Salary
from app.models.overtime import Overtime
from app.services.insurance_calculator import InsuranceCalculator
from app.services.benefit_calculator import BenefitCalculator
from app.services.tax_engine import compute_tax_for_date

class ComprehensiveSalaryCalculator:
    """حاسبة رواتب شاملة احترافية"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def calculate(self, salary_id: int) -> dict:
        """حساب راتب كامل مع كل التفاصيل"""
        
        salary = self.session.exec(
            select(Salary).where(Salary.id == salary_id)
        ).first()
        
        if not salary:
            raise Exception(f"سجل الراتب {salary_id} غير موجود")
        
        emp = self.session.exec(
            select(Employee).where(Employee.id == salary.employee_id)
        ).first()
        
        if not emp:
            raise Exception(f"الموظف {salary.employee_id} غير موجود")
        
        # حاسبات مساعدة
        insurance_calc = InsuranceCalculator(self.session)
        benefit_calc = BenefitCalculator(self.session)
        
        payment_date = salary.payment_date or date(salary.salary_year, salary.salary_month, 1)
        basic = salary.basic_salary
        
        # 1️⃣ حساب ساعات إضافية
        hourly_rate = basic / 30 / 8  # أجر الساعة = أساسي ÷ 30 يوم ÷ 8 ساعات
        
        day_overtime = salary.extra_hours_value * 1.35 if salary.extra_hours > 0 else 0
        # ملاحظة: يفترض أن extra_hours_value محسوبة بالفعل، لو في تفصيل أكتر نحتاج حقل آخر للساعات الليلية
        
        # 2️⃣ فصل البدلات
        benefits = benefit_calc.separate_benefits(salary_id)
        in_kind_total = benefits["in_kind"]["total"]
        cash_benefits = benefits["cash"]["allowances"]
        
        # 3️⃣ إجمالي الاستحقاقات
        total_earnings = (
            basic +
            salary.bonus_performance +
            salary.bonus_project +
            salary.other_earnings +
            day_overtime +
            in_kind_total +  # البدلات العينية (ستُخصم لاحقاً)
            cash_benefits    # البدلات النقدية (لا تُخصم)
        )
        
        # 4️⃣ التأمينات
        employee_insurance = insurance_calc.calculate_employee_insurance(emp.id, basic)
        employer_insurance = insurance_calc.calculate_employer_insurance(emp.id, basic)
        
        # 5️⃣ الضرائب
        # الوعاء الضريبي = الاستحقاقات - التأمين الاجتماعي - الإعفاء
        personal_exemption_monthly = 15000 / 12
        taxable_base = total_earnings - employee_insurance["social_insurance"] - personal_exemption_monthly
        
        if taxable_base > 0:
            tax_income = compute_tax_for_date(self.session, taxable_base, payment_date)
        else:
            tax_income = 0
        
        # 6️⃣ إجمالي الاستقطاعات
        total_deductions = (
            employee_insurance["total"] +
            tax_income +
            salary.deduction_absence +
            salary.deduction_penalties +
            salary.deduction_other +
            in_kind_total  # خصم البدلات العينية التي تم إضافتها أعلى
        )
        
        # 7️⃣ الراتب المستحق
        salary_due = total_earnings - total_deductions
        
        # 8️⃣ الصافي النهائي
        net_salary = salary_due - (salary.advance_salary + salary.loan_deduction)
        
        # تحديث السجل
        salary.total_earnings = round(total_earnings, 2)
        salary.total_deductions = round(total_deductions, 2)
        salary.salary_due = round(salary_due, 2)
        salary.net_salary = round(net_salary, 2)
        salary.deduction_insurance_social_employee = round(employee_insurance["social_insurance"], 2)
        salary.deduction_insurance_health = round(employee_insurance["health_insurance"], 2)
        salary.deduction_tax_income = round(tax_income, 2)
        salary.updated_at = datetime.utcnow()
        
        self.session.add(salary)
        self.session.commit()
        
        return {
            "employee_id": emp.id,
            "employee_name": emp.name,
            "period": f"{salary.salary_year}-{salary.salary_month:02d}",
            
            "earnings": {
                "basic_salary": round(basic, 2),
                "overtime": round(day_overtime, 2),
                "bonuses": round(salary.bonus_performance + salary.bonus_project, 2),
                "benefits": {
                    "in_kind": benefits["in_kind"],
                    "cash": benefits["cash"]
                },
                "other": round(salary.other_earnings, 2),
                "total": round(total_earnings, 2),
            },
            
            "deductions": {
                "insurance_employee": employee_insurance,
                "tax": round(tax_income, 2),
                "administrative": {
                    "absence": round(salary.deduction_absence, 2),
                    "penalties": round(salary.deduction_penalties, 2),
                    "other": round(salary.deduction_other, 2),
                },
                "in_kind_deduction": round(in_kind_total, 2),
                "total": round(total_deductions, 2),
            },
            
            "salary_due": round(salary_due, 2),
            
            "final_deductions": {
                "advance": round(salary.advance_salary, 2),
                "loans": round(salary.loan_deduction, 2),
                "total": round(salary.advance_salary + salary.loan_deduction, 2),
            },
            
            "net_salary": round(net_salary, 2),
            
            "employer_costs": employer_insurance,
        }