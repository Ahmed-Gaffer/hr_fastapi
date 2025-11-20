from datetime import datetime, date
from sqlmodel import Session, select
from app.models.employee import Employee
from app.models.salary_record import SalaryRecord, PayrollCategory
from app.models.salary_config import SalaryConfig
from app.services.tax_engine import compute_tax_for_date

class ProfessionalSalaryCalculator:
    """حاسبة رواتب احترافية"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def calculate(self, salary_record_id: int) -> dict:
        """حساب شامل للراتب"""
        
        salary = self.session.exec(
            select(SalaryRecord).where(SalaryRecord.id == salary_record_id)
        ).first()
        
        if not salary:
            raise Exception(f"سجل الراتب {salary_record_id} غير موجود")
        
        emp = self.session.exec(
            select(Employee).where(Employee.id == salary.employee_id)
        ).first()
        
        if not emp:
            raise Exception(f"الموظف {salary.employee_id} غير موجود")
        
        config = self._get_config(salary.salary_year)
        payment_date = salary.payment_date or date(salary.salary_year, salary.salary_month, 1)
        
        # 🟢 1️⃣ إجمالي الاستحقاقات
        total_earnings = (
            salary.basic_salary +
            salary.allowance_food +
            salary.allowance_transport +
            salary.allowance_travel +
            salary.allowance_position +
            salary.extra_hours_value +
            salary.bonus_performance +
            salary.bonus_project +
            salary.other_earnings
        )
        
        # 🔵 2️⃣ خصومات حكومية (من الأساسي فقط)
        insurance_social = salary.basic_salary * config.insurance_social_employee_rate
        insurance_health = salary.basic_salary * config.insurance_health_rate
        
        # ضريبة كسب العمل
        personal_exemption_monthly = config.personal_exemption_annual / 12
        taxable_base = total_earnings - insurance_social - personal_exemption_monthly
        
        if taxable_base > 0:
            tax_income = compute_tax_for_date(self.session, taxable_base, payment_date)
        else:
            tax_income = 0
        
        # إجمالي الاستقطاعات
        total_deductions = (
            insurance_social +
            insurance_health +
            tax_income +
            salary.deduction_absence +
            salary.deduction_penalties +
            salary.deduction_other
        )
        
        # 🟡 3️⃣ الراتب المستحق
        salary_due = total_earnings - total_deductions
        
        # 🟠 4️⃣ الصافي النهائي
        net_salary = salary_due - (salary.advance_salary + salary.loan_deduction)
        
        # تحديث السجل
        salary.total_earnings = round(total_earnings, 2)
        salary.deduction_insurance_social_employee = round(insurance_social, 2)
        salary.deduction_insurance_health = round(insurance_health, 2)
        salary.deduction_tax_income = round(tax_income, 2)
        salary.total_deductions = round(total_deductions, 2)
        salary.salary_due = round(salary_due, 2)
        salary.net_salary = round(net_salary, 2)
        salary.updated_at = datetime.utcnow()
        
        self.session.add(salary)
        self.session.commit()
        
        return {
            "employee_id": emp.id,
            "employee_name": emp.name,
            "period": f"{salary.salary_year}-{salary.salary_month:02d}",
            "category": salary.payroll_category,
            "earnings": {
                "basic_salary": round(salary.basic_salary, 2),
                "allowances": {
                    "food": round(salary.allowance_food, 2),
                    "transport": round(salary.allowance_transport, 2),
                    "travel": round(salary.allowance_travel, 2),
                    "position": round(salary.allowance_position, 2),
                },
                "extra_hours": round(salary.extra_hours_value, 2),
                "bonuses": {
                    "performance": round(salary.bonus_performance, 2),
                    "project": round(salary.bonus_project, 2),
                },
                "other_earnings": round(salary.other_earnings, 2),
                "total": round(total_earnings, 2),
            },
            "deductions": {
                "government": {
                    "social_insurance": round(insurance_social, 2),
                    "health_insurance": round(insurance_health, 2),
                    "income_tax": round(tax_income, 2),
                },
                "administrative": {
                    "absence": round(salary.deduction_absence, 2),
                    "penalties": round(salary.deduction_penalties, 2),
                    "other": round(salary.deduction_other, 2),
                },
                "total": round(total_deductions, 2),
            },
            "salary_due": round(salary_due, 2),
            "final_deductions": {
                "advance_salary": round(salary.advance_salary, 2),
                "loan": round(salary.loan_deduction, 2),
                "total": round(salary.advance_salary + salary.loan_deduction, 2),
            },
            "net_salary": round(net_salary, 2),
            "verification": {
                "step1": f"{salary.basic_salary} + {salary.allowance_food + salary.allowance_transport + salary.allowance_travel + salary.allowance_position} + {salary.extra_hours_value} + {salary.bonus_performance + salary.bonus_project} + {salary.other_earnings} = {total_earnings}",
                "step2": f"{total_earnings} - ({insurance_social} + {insurance_health} + {tax_income} + {salary.deduction_absence + salary.deduction_penalties + salary.deduction_other}) = {salary_due}",
                "step3": f"{salary_due} - ({salary.advance_salary} + {salary.loan_deduction}) = {net_salary}",
            }
        }
    
    def _get_config(self, year: int) -> SalaryConfig:
        config = self.session.exec(
            select(SalaryConfig).where(SalaryConfig.year == year)
        ).first()
        return config or SalaryConfig(year=year)