# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models/__init__.py
# File Name: __init__.py
# -----------------------------------------

# __init__.py داخل app/models
# الهدف: توحيد الاستيرادات لكل الموديلات علشان يبقى عندك نقطة نظام واضحة

from .tenant import Tenant, TenantStatus
from .site import Site
from .project import Project
from .cost_center import CostCenter
from .department import Department
from .employee import Employee, WorkStatus, InsuranceStatus, EmployeeStatus
from .employee_details import EmployeeDetails
from .attendance import Attendance
from .salary import SalaryRecord, PayrollCategory
from .salary_component import SalaryComponent, ComponentType
from .salary_config import SalaryConfig
from .company_config import CompanyConfig
from .benefit_record import BenefitRecord, BenefitType
from .overtime_record import OvertimeRecord
from .tax_policy import TaxPolicy
