from datetime import datetime, date
from sqlmodel import Session, select
from app.models.salary_record import SalaryRecord, PayrollCategory
from app.models.employee import Employee
from app.services.professional_salary_calculator import ProfessionalSalaryCalculator

class SmartSalaryImporter:
    """
    استيراد ذكي:
    - بيانات قديمة (60 شهر): احفظها كما هي بدون حسابات
    - آخر شهر: احسبه من الأول وقارن مع الملف
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def import_salary_record(self, salary_data: dict, is_last_month: bool = False) -> dict:
        """
        استيراد سجل راتب واحد
        
        Args:
            salary_data: dict يحتوي على بيانات الراتب
            is_last_month: True إذا كان آخر شهر في الملف (سيتم التحقق منه)
        
        Returns:
            dict يحتوي على:
            - السجل المحفوظ
            - نتائج التحقق (إن وجدت)
            - أي تحذيرات/أخطاء
        """
        
        emp_id = salary_data.get("employee_id")
        year = salary_data.get("year")
        month = salary_data.get("month")
        
        # تحقق من وجود الموظف
        emp = self.session.exec(
            select(Employee).where(Employee.id == emp_id)
        ).first()
        if not emp:
            return {"status": "error", "message": f"الموظف {emp_id} غير موجود"}
        
        # تحقق من عدم تكرار السجل
        exists = self.session.exec(
            select(SalaryRecord).where(
                SalaryRecord.employee_id == emp_id,
                SalaryRecord.salary_year == year,
                SalaryRecord.salary_month == month
            )
        ).first()
        if exists:
            return {"status": "error", "message": f"سجل راتب موجود بالفعل"}
        
        # أنشئ السجل من البيانات المدخلة
        sal = SalaryRecord(
            employee_id=emp_id,
            salary_year=year,
            salary_month=month,
            payroll_category=salary_data.get("payroll_category", PayrollCategory.CATEGORY_A),
            basic_salary=salary_data.get("basic_salary", 0),
            allowance_food=salary_data.get("allowance_food", 0),
            allowance_transport=salary_data.get("allowance_transport", 0),
            allowance_travel=salary_data.get("allowance_travel", 0),
            allowance_position=salary_data.get("allowance_position", 0),
            extra_hours=salary_data.get("extra_hours", 0),
            extra_hours_value=salary_data.get("extra_hours_value", 0),
            bonus_performance=salary_data.get("bonus_performance", 0),
            bonus_project=salary_data.get("bonus_project", 0),
            other_earnings=salary_data.get("other_earnings", 0),
            deduction_insurance_social_employee=salary_data.get("deduction_insurance_social_employee", 0),
            deduction_insurance_health=salary_data.get("deduction_insurance_health", 0),
            deduction_absence=salary_data.get("deduction_absence", 0),
            deduction_penalties=salary_data.get("deduction_penalties", 0),
            deduction_other=salary_data.get("deduction_other", 0),
            advance_salary=salary_data.get("advance_salary", 0),
            loan_deduction=salary_data.get("loan_deduction", 0),
            attendance_days=salary_data.get("attendance_days", 30),
            absence_days=salary_data.get("absence_days", 0),
            payment_date=salary_data.get("payment_date"),
            notes=salary_data.get("notes")
        )
        
        self.session.add(sal)
        self.session.flush()
        
        result = {
            "status": "saved",
            "salary_record_id": sal.id,
            "employee_name": emp.name,
            "period": f"{year}-{month:02d}",
            "message": "تم حفظ السجل"
        }
        
        # 🔍 إذا كان آخر شهر → احسبه والقارن
        if is_last_month:
            calc = ProfessionalSalaryCalculator(self.session)
            calculated = calc.calculate(sal.id)
            
            # جيب الصافي من الملف
            file_net_salary = salary_data.get("net_salary_from_file", 0)
            calculated_net_salary = calculated.get("net_salary", 0)
            
            # قارن
            difference = abs(file_net_salary - calculated_net_salary)
            
            result["verification"] = {
                "file_net_salary": file_net_salary,
                "calculated_net_salary": calculated_net_salary,
                "difference": round(difference, 2),
                "match": difference < 1,  # تطابق إذا كان الفرق أقل من 1 جنيه
                "calculation_details": calculated
            }
            
            if not result["verification"]["match"]:
                result["warnings"] = [
                    f"⚠️ فرق في الراتب الصافي: {round(difference, 2)} جنيه",
                    f"الملف: {file_net_salary} | المحسوب: {calculated_net_salary}"
                ]
        
        return result