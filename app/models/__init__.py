# __init__.py داخل app/models
# -----------------------------------------
# الهدف: توحيد الاستيرادات لكل الموديلات علشان يبقى عندك نقطة نظام واضحة

# 🟢 الموديلات الأساسية
from .tenant import Tenant, TenantStatus
from .site import Site
from .project import Project
from .cost_center import CostCenter
from .department import Department
from .employee import Employee, WorkStatus, InsuranceStatus, EmployeeStatus
from .employee_details import EmployeeDetails
from .attendance import Attendance
from .salary import Salary, PayrollCategory
from .salary_component import SalaryComponent, ComponentType
from .salary_config import SalaryConfig
from .company_config import CompanyConfig
from .benefit import Benefit, BenefitType
from .overtime import Overtime
from .tax_policy import TaxPolicy
from .user import User

# 🟢 level1 → employee_plus
from .levels.level1.employee_plus.Employee_AdvanceSalary import Employee_AdvanceSalary
from .levels.level1.employee_plus.employee_asset import Employee_Asset
from .levels.level1.employee_plus.Employee_Attendance import Employee_Attendance
from .levels.level1.employee_plus.Employee_Benefit import Employee_Benefit
from .levels.level1.employee_plus.employee_certification import Employee_Certification
from .levels.level1.employee_plus.Employee_Configuration import Employee_Configuration
from .levels.level1.employee_plus.Employee_CostCenter import Employee_CostCenter
from .levels.level1.employee_plus.Employee_Deduction import Employee_Deduction
from .levels.level1.employee_plus.employee_department import Employee_Department
from .levels.level1.employee_plus.Employee_Disciplinary import Employee_Disciplinary
from .levels.level1.employee_plus.employee_leave import Employee_Leave, LeaveType
from .levels.level1.employee_plus.Employee_Loan import Employee_Loan
from .levels.level1.employee_plus.Employee_PerformanceReview import Employee_PerformanceReview
from .levels.level1.employee_plus.employee_policy import Employee_Policy
from .levels.level1.employee_plus.employee_project import Employee_Project
from .levels.level1.employee_plus.Employee_PublicHoliday import Employee_PublicHoliday
from .levels.level1.employee_plus.Employee_Reward import Employee_Reward
from .levels.level1.employee_plus.employee_role import Employee_Role
from .levels.level1.employee_plus.Employee_Salary import Employee_Salary
from .levels.level1.employee_plus.employee_skill import Employee_Skill
from .levels.level1.employee_plus.Employee_Tenant import Employee_Tenant
from .levels.level1.employee_plus.employee_training import Employee_Training
from .levels.level1.employee_plus.Employee_User import Employee_User

# 🟢 level1 → Intermediate
from .levels.level1.Intermediate.Asset_Site import Asset_Site
from .levels.level1.Intermediate.Department_Configuration import Department_Configuration
from .levels.level1.Intermediate.Department_Policy import Department_Policy
from .levels.level1.Intermediate.Department_Site import Department_Site
from .levels.level1.Intermediate.Project_Asset import Project_Asset
from .levels.level1.Intermediate.Project_Configuration import Project_Configuration
from .levels.level1.Intermediate.Project_Department import Project_Department
from .levels.level1.Intermediate.Project_Policy import Project_Policy
from .levels.level1.Intermediate.project_site import Project_Site
from .levels.level1.Intermediate.Tenant_Configuration import Tenant_Configuration
from .levels.level1.Intermediate.Tenant_Department import Tenant_Department
from .levels.level1.Intermediate.Tenant_Policy import Tenant_Policy
from .levels.level1.Intermediate.Tenant_Site import Tenant_Site
from .levels.level1.Intermediate.Training_Project import Training_Project

# 🟢 level1 → units
from .levels.level1.units.AdvanceSalary import AdvanceSalary
from .levels.level1.units.DisciplinaryAction import DisciplinaryAction
from .levels.level1.units.Loan import Loan
from .levels.level1.units.PerformanceReview import PerformanceReview
from .levels.level1.units.PublicHoliday import PublicHoliday
from .levels.level1.units.Reward import Reward

# 🟢 level2
from .levels.level2.Employee_Asset_Site import Employee_Asset_Site
from .levels.level2.Employee_Department_Role import Employee_Department_Role
from .levels.level2.Employee_Department_Site import Employee_Department_Site
from .levels.level2.Employee_Policy_CostCenter import Employee_Policy_CostCenter
from .levels.level2.Employee_Project_CostCenter import Employee_Project_CostCenter
from .levels.level2.Employee_Project_Site import Employee_Project_Site
from .levels.level2.Employee_Site_Role import Employee_Site_Role
from .levels.level2.Employee_Training_Certification import Employee_Training_Certification
from .levels.level2.Project_Department_Policy import Project_Department_Policy
from .levels.level2.Project_Employee_Role import Project_Employee_Role

# 🟢 level3
from .levels.level3.Employee_Asset_Project_Site import Employee_Asset_Project_Site
from .levels.level3.Employee_Asset_Site_Role import Employee_Asset_Site_Role
from .levels.level3.Employee_Project_Role_CostCenter import Employee_Project_Role_CostCenter
from .levels.level3.Employee_Project_Site_CostCenter import Employee_Project_Site_CostCenter
from .levels.level3.Employee_Project_Site_Department import Employee_Project_Site_Department
from .levels.level3.Employee_Training_Certification_Project import Employee_Training_Certification_Project
from .levels.level3.Employee_Training_Project_Site import Employee_Training_Project_Site
from .levels.level3.Tenant_Site_Department_CostCenter import Tenant_Site_Department_CostCenter

# 🟢 level4
from .levels.level4.Employee_Asset_Project_Site_Role import Employee_Asset_Project_Site_Role
from .levels.level4.Employee_Training_Certification_Project_Site import Employee_Training_Certification_Project_Site
from .levels.level4.Tenant_Site_Department_CostCenter_Policy import Tenant_Site_Department_CostCenter_Policy
