from datetime import datetime
from sqlmodel import Session, select
from app.models.employee import Employee
from app.models.salary_record import SalaryRecord
from app.models.salary_component import SalaryComponent, ComponentType
from app.models.salary_config import SalaryConfig
from app.services.tax_engine import compute_tax_for_date

class AdvancedSalaryCalculator:
    """
    حاسبة رواتب احترافية متقدمة:
    - تدعم كل البنود الأساسية والإضافية
    - مرنة للتوسع المستقبلي
    - معادلات مصرية دقيقة
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_config(self, year: int) -> SalaryConfig:
        """احصل على إعدادات السنة أو استخدم الافتراضية"""
        config = self.session.exec(
            select(SalaryConfig).where(SalaryConfig.year == year)
        ).first()
        
        if not config:
            config = SalaryConfig(year=year)
        
        return config
    
    def calculate(self, salary_record_id: int) -> dict:
        """
        حساب شامل للراتب مع كل البنود
        
        المعادلة المصرية:
        1. الراتب الإجمالي = أساسي + بدلات + ساعات إضافية + مكافآت
        2. الخصومات = تأمين + أقساط + سلف + خصومات موقع
        3. الوعاء الضريبي = الراتب - التأمين - الإعفاء
        4. الضريبة = الوعاء × 20%
        5. الصافي = الراتب - الخصومات - الضريبة
        """
        
        # احصل على سجل الراتب
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
        
        config = self.get_config(salary.salary_year)
        
        # 🟢 1️⃣ الراتب الأساسي والبدلات الثابتة
        base = salary.base_salary
        allowances = (
            salary.allowance_food +
            salary.allowance_transport +
            salary.allowance_travel +
            salary.allowance_position
        )
        
        # 🟢 2️⃣ احسب بنود إضافية (ساعات إضافية، مكافآت)
        extra_components = self.session.exec(
            select(SalaryComponent).where(
                SalaryComponent.salary_record_id == salary_record_id,
                SalaryComponent.is_deduction == False
            )
        ).all()
        
        extra_allowances = sum(c.amount for c in extra_components)
        
        # الراتب الإجمالي قبل الخصومات
        total_salary_before_deductions = base + allowances + extra_allowances
        
        # 🔵 3️⃣ الخصومات الثابتة
        # التأمين الاجتماعي = 11% من الأساسي فقط
        insurance_social_employee = base * config.insurance_social_employee_rate
        
        # التأمين الصحي = 2% من الأساسي
        insurance_health = base * config.insurance_health_rate
        
        # أقساط وسلف
        fixed_deductions = (
            insurance_social_employee +
            insurance_health +
            salary.deduction_loans +
            salary.deduction_advance
        )
        
        # 🔵 4️⃣ احسب خصومات إضافية (خصم موقع، خصومات خاصة)
        extra_deductions_components = self.session.exec(
            select(SalaryComponent).where(
                SalaryComponent.salary_record_id == salary_record_id,
                SalaryComponent.is_deduction == True
            )
        ).all()
        
        extra_deductions = sum(c.amount for c in extra_deductions_components)
        
        total_deductions_non_tax = fixed_deductions + extra_deductions
        
        # 🟡 5️⃣ حساب الضرائب (معادلة كسب العمل المصرية)
        personal_exemption_monthly = config.personal_exemption_annual / 12
        taxable_base = total_salary_before_deductions - insurance_social_employee - personal_exemption_monthly
        if taxable_base > 0:
            monthly_tax = compute_tax_for_date(self.session, taxable_base, salary.payment_date or date(salary.salary_year, salary.salary_month, 1))
        else:
            monthly_tax = 0
        
        # 📊 6️⃣ الصافي النهائي
        net_salary = total_salary_before_deductions - total_deductions_non_tax - monthly_tax
        
        # 💼 7️⃣ معلومات صاحب العمل (للمراجعة فقط)
        insurance_employer = base * config.insurance_social_employer_rate
        
        # تحديث السجل بالحسابات
        salary.total_salary_before_deductions = round(total_salary_before_deductions, 2)
        salary.total_deductions = round(total_deductions_non_tax + monthly_tax, 2)
        salary.net_salary = round(net_salary, 2)
        salary.tax_monthly = round(monthly_tax, 2)
        salary.tax_annual = round(annual_tax, 2)
        salary.taxable_base = round(taxable_base, 2)
        salary.updated_at = datetime.utcnow()
        
        self.session.add(salary)
        self.session.commit()
        
        return {
            "employee_id": emp.id,
            "employee_name": emp.name,
            "period": f"{salary.salary_year}-{salary.salary_month:02d}",
            
            # 📊 الراتب الأساسي والبدلات
            "breakdown": {
                "salary": {
                    "base_salary": round(base, 2),
                    "allowances": {
                        "food": round(salary.allowance_food, 2),
                        "transport": round(salary.allowance_transport, 2),
                        "travel": round(salary.allowance_travel, 2),
                        "position": round(salary.allowance_position, 2),
                    },
                    "total_allowances": round(allowances, 2),
                    "extra_allowances": round(extra_allowances, 2),
                },
                "deductions": {
                    "insurance": {
                        "social_employee": round(insurance_social_employee, 2),
                        "health": round(insurance_health, 2),
                    },
                    "other": {
                        "loans": round(salary.deduction_loans, 2),
                        "advance": round(salary.deduction_advance, 2),
                    },
                    "extra_deductions": round(extra_deductions, 2),
                    "total_deductions": round(total_deductions_non_tax, 2),
                },
                "tax": {
                    "taxable_base": round(taxable_base, 2),
                    "monthly": round(monthly_tax, 2),
                    "annual": round(annual_tax, 2),
                },
            },
            
            # 💰 الإجماليات
            "totals": {
                "total_salary_before_deductions": round(total_salary_before_deductions, 2),
                "total_deductions_and_tax": round(total_deductions_non_tax + monthly_tax, 2),
                "net_salary": round(net_salary, 2),
            },
            
            # 👔 معلومات صاحب العمل
            "employer_costs": {
                "insurance_social": round(insurance_employer, 2),
            },
            
            # ✅ معادلة التحقق
            "verification": {
                "step1": f"أساسي ({base}) + بدلات ({allowances}) + إضافيات ({extra_allowances}) = {total_salary_before_deductions}",
                "step2": f"خصومات = تأمين ({insurance_social_employee + insurance_health}) + أقساط ({salary.deduction_loans + salary.deduction_advance}) + إضافي ({extra_deductions}) = {total_deductions_non_tax}",
                "step3": f"وعاء ضريبي = {total_salary_before_deductions} - {insurance_social_employee} - {personal_exemption_monthly} = {taxable_base}",
                "step4": f"ضريبة = {taxable_base} × 20% = {monthly_tax}",
                "step5": f"صافي = {total_salary_before_deductions} - {total_deductions_non_tax} - {monthly_tax} = {net_salary}",
            }
        }
    
    def add_component(self, salary_record_id: int, component_type: str, 
                     description: str, quantity: float, unit_rate: float, 
                     is_deduction: bool = False) -> SalaryComponent:
        """أضف بند إضافي للراتب (ساعات إضافية، مكافآت، خصومات)"""
        
        amount = quantity * unit_rate
        component = SalaryComponent(
            salary_record_id=salary_record_id,
            component_type=component_type,
            description=description,
            quantity=quantity,
            unit_rate=unit_rate,
            amount=amount,
            is_deduction=is_deduction
        )
        
        self.session.add(component)
        self.session.commit()
        
        return component