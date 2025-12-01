# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\services\salary_calculator.py
# File Name: salary_calculator.py
# -----------------------------------------

from datetime import datetime, date
from sqlmodel import Session, select
from app.models.employee import Employee
from app.models.salary import SalaryRecord

class TaxConfig:
    """معادلات الضرائب والتأمينات المصرية 2024-2025"""
    
    # ✅ تأمين اجتماعي (موظف) = 11% من الراتب الأساسي
    EMPLOYEE_INSURANCE_RATE = 0.11
    
    # ✅ تأمين اجتماعي (صاحب عمل) = 19% من الراتب الأساسي
    EMPLOYER_INSURANCE_RATE = 0.19
    
    # ✅ تأمين صحي شامل = 2% من الراتب (موظف)
    HEALTH_INSURANCE_RATE = 0.02
    
    # ✅ الإعفاء الشخصي السنوي = 15,000 جنيه
    PERSONAL_EXEMPTION = 15000
    
    # ✅ معدل ضريبة كسب العمل = 20%
    TAX_RATE = 0.20
    
    # ✅ الحد الأدنى للراتب الخاضع للضريبة
    MIN_TAXABLE = 3000
    
    # ✅ الرقم الأساسي لحساب الضريبة التصاعدية
    TAX_BASE_MONTHLY = PERSONAL_EXEMPTION / 12  # 1,250 شهرياً

class SalaryCalculator:
    """حسابة رواتب احترافية - معادلات مصرية"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def calculate_salary(self, employee_id: int, year: int, month: int) -> dict:
        """
        حساب راتب موظف للشهر المحدد
        
        المعادلة:
        1. الراتب الأساسي + البدلات = الراتب الإجمالي
        2. الخصومات التأمينية:
           - تأمين اجتماعي (موظف) = 11% من الأساسي
           - تأمين صحي = 2% من الأساسي
           - أقساط وسلف = كما هي
        3. الضرائب:
           - الوعاء الخاضع = الراتب - التأمين - الإعفاء الشهري
           - الضريبة = الوعاء × 20% (إن كان > 3,000)
        4. الصافي = الراتب الإجمالي - الخصومات - الضرائب
        """
        
        emp = self.session.exec(
            select(Employee).where(Employee.id == employee_id)
        ).first()
        
        if not emp:
            raise Exception(f"الموظف {employee_id} غير موجود")
        
        # 1️⃣ الراتب الأساسي والبدلات
        base = emp.base_salary or 0
        
        # 2️⃣ البدلات الشهرية (افترض أنها محفوظة في جدول أو مأخوذة من الإدخال)
        food = 2500 if base > 10000 else 1500  # إعاشة افتراضية (يمكن تعديلها)
        transport = 1000  # مواصلات
        travel = 400  # سفر
        other = 0  # بدلات أخرى
        
        total_allowances = food + transport + travel + other
        total_salary_before_deductions = base + total_allowances
        
        # 3️⃣ الخصومات التأمينية
        # تأمين اجتماعي (موظف) = 11% من الأساسي فقط (NOT البدلات)
        insurance_employee = base * TaxConfig.EMPLOYEE_INSURANCE_RATE
        
        # تأمين صحي شامل = 2%
        health_insurance = base * TaxConfig.HEALTH_INSURANCE_RATE
        
        # أقساط / سلف (مأخوذة من الإدخال أو 0)
        loans = 0
        advance = 0
        
        total_deductions = insurance_employee + health_insurance + loans + advance
        
        # 4️⃣ الضرائب (معادلة كسب العمل)
        # الوعاء الخاضع = الراتب الإجمالي - التأمين - الإعفاء
        taxable_base = total_salary_before_deductions - insurance_employee - TaxConfig.TAX_BASE_MONTHLY
        
        if taxable_base > TaxConfig.MIN_TAXABLE:
            monthly_tax = taxable_base * TaxConfig.TAX_RATE
            annual_tax = monthly_tax * 12
        else:
            monthly_tax = 0
            annual_tax = 0
        
        # 5️⃣ الصافي النهائي
        net_salary = total_salary_before_deductions - total_deductions - monthly_tax
        
        # 6️⃣ تأمين صاحب العمل (معلومة فقط، لا تدخل الحساب)
        employer_insurance = base * TaxConfig.EMPLOYER_INSURANCE_RATE
        
        return {
            "employee_id": employee_id,
            "employee_name": emp.name,
            "year": year,
            "month": month,
            # الراتب الأساسي والبدلات
            "base_salary": base,
            "food_allowance": food,
            "transport_allowance": transport,
            "travel_allowance": travel,
            "other_allowances": other,
            "total_allowances": total_allowances,
            "total_salary_before_deductions": total_salary_before_deductions,
            # الخصومات
            "insurance_employee": round(insurance_employee, 2),
            "health_insurance": round(health_insurance, 2),
            "loans": loans,
            "advance_salary": advance,
            "total_deductions_non_tax": round(total_deductions, 2),
            # الضرائب
            "taxable_base": round(taxable_base, 2),
            "monthly_tax": round(monthly_tax, 2),
            "annual_tax": round(annual_tax, 2),
            # معلومات صاحب العمل
            "employer_insurance": round(employer_insurance, 2),
            # الصافي النهائي
            "net_salary": round(net_salary, 2),
            # للتحقق
            "formula_check": {
                "step1": f"أساسي + بدلات = {base} + {total_allowances} = {total_salary_before_deductions}",
                "step2": f"خصومات = تأمين ({insurance_employee:.2f}) + صحي ({health_insurance:.2f}) + أقساط ({loans}) = {total_deductions:.2f}",
                "step3": f"وعاء ضريبي = {total_salary_before_deductions} - {insurance_employee:.2f} - {TaxConfig.TAX_BASE_MONTHLY} = {taxable_base:.2f}",
                "step4": f"ضريبة شهرية = {taxable_base:.2f} × 20% = {monthly_tax:.2f}",
                "step5": f"صافي = {total_salary_before_deductions} - {total_deductions:.2f} - {monthly_tax:.2f} = {net_salary:.2f}"
            }
        }