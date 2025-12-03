# __init__.py داخل app/models
# -----------------------------------------
# الهدف: توحيد الاستيرادات لكل الموديلات علشان يبقى عندك نقطة نظام واضحة

# 🟢 الموديلات الأساسية
from .tenant import Tenant, TenantStatus
from .site import Site
from .project import Project
from .cost_center import Costcenter
from .department import Department
from .employee import Employee, Workstatus, Insurancestatus, EmployeeStatus
from .employee_details import Employeedetails
from .attendance import Attendance
from .salary import Salaryrecord, Payrollcategory
from .salary_component import SalaryComponent, Componenttype
from .salary_config import SalaryConfig
from .company_config import CompanyConfig
from .benefit_record import BenefitRecord, Benefittype
from .overtime_record import OvertimeRecord
from .tax_policy import TaxPolicy
from .user import User

# 🟢 level1 → employee_plus
from .levels.level1.employee_plus.employee_advance_salary import EmployeeAdvancesalary
from .levels.level1.employee_plus.employee_asset import EmployeeAsset
from .levels.level1.employee_plus.employee_attendance_record import EmployeeAttendancerecord
from .levels.level1.employee_plus.employee_benefit_record import EmployeeBenefitrecord
from .levels.level1.employee_plus.employee_certification import EmployeeCertification
from .levels.level1.employee_plus.employee_configuration import EmployeeConfiguration
from .levels.level1.employee_plus.employee_cost_center import EmployeeCostcenter
from .levels.level1.employee_plus.employee_deduction_record import EmployeeDeductionrecord
from .levels.level1.employee_plus.employee_department import EmployeeDepartment
from .levels.level1.employee_plus.employee_disciplinary import EmployeeDisciplinary
from .levels.level1.employee_plus.employee_leave import EmployeeLeave, Leavetype
from .levels.level1.employee_plus.employee_loan import EmployeeLoan
from .levels.level1.employee_plus.employee_performance_review import EmployeePerformancereview
from .levels.level1.employee_plus.employee_policy import EmployeePolicy
from .levels.level1.employee_plus.employee_project import EmployeeProject
from .levels.level1.employee_plus.employee_public_holiday import EmployeePublicholiday
from .levels.level1.employee_plus.employee_reward import EmployeeReward
from .levels.level1.employee_plus.employee_role import EmployeeRole
from .levels.level1.employee_plus.employee_salary_record import EmployeeSalaryrecord
from .levels.level1.employee_plus.employee_skill import EmployeeSkill
from .levels.level1.employee_plus.employee_tenant import EmployeeTenant
from .levels.level1.employee_plus.employee_training import EmployeeTraining
from .levels.level1.employee_plus.employee_user import EmployeeUser

# 🟢 level1 → Intermediate
from .levels.level1.Intermediate.asset_site import AssetSite
from .levels.level1.Intermediate.department_configuration import DepartmentConfiguration
from .levels.level1.Intermediate.department_policy import DepartmentPolicy
from .levels.level1.Intermediate.department_site import DepartmentSite
from .levels.level1.Intermediate.project_asset import ProjectAsset
from .levels.level1.Intermediate.project_configuration import ProjectConfiguration
from .levels.level1.Intermediate.project_department import ProjectDepartment
from .levels.level1.Intermediate.project_policy import ProjectPolicy
from .levels.level1.Intermediate.project_site import ProjectSite
from .levels.level1.Intermediate.tenant_configuration import TenantConfiguration
from .levels.level1.Intermediate.tenant_department import TenantDepartment
from .levels.level1.Intermediate.tenant_policy import TenantPolicy
from .levels.level1.Intermediate.tenant_site import TenantSite
from .levels.level1.Intermediate.training_project import TrainingProject

# 🟢 level1 → units
from .levels.level1.units.advance_salary import Advancesalary
from .levels.level1.units.disciplinary_action import Disciplinaryaction
from .levels.level1.units.loan import Loan
from .levels.level1.units.performance_review import Performancereview
from .levels.level1.units.public_holiday import Publicholiday
from .levels.level1.units.reward import Reward

# 🟢 level2
from .levels.level2.employee_asset_site import EmployeeAssetSite
from .levels.level2.employee_department_role import EmployeeDepartmentRole
from .levels.level2.employee_department_site import EmployeeDepartmentSite
from .levels.level2.employee_policy_cost_center import EmployeePolicyCostcenter
from .levels.level2.employee_project_cost_center import EmployeeProjectCostcenter
from .levels.level2.employee_project_site import EmployeeProjectSite
from .levels.level2.employee_site_role import EmployeeSiteRole
from .levels.level2.employee_training_certification import EmployeeTrainingCertification
from .levels.level2.project_department_policy import ProjectDepartmentPolicy
from .levels.level2.project_employee_role import ProjectEmployeeRole

# 🟢 level3
from .levels.level3.employee_asset_project_site import EmployeeAssetProjectSite
from .levels.level3.employee_asset_site_role import EmployeeAssetSiteRole
from .levels.level3.employee_project_role_cost_center import EmployeeProjectRoleCostcenter
from .levels.level3.employee_project_site_cost_center import EmployeeProjectSiteCostcenter
from .levels.level3.employee_project_site_department import EmployeeProjectSiteDepartment
from .levels.level3.employee_training_certification_project import EmployeeTrainingCertificationProject
from .levels.level3.employee_training_project_site import EmployeeTrainingProjectSite
from .levels.level3.tenant_site_department_cost_center import TenantSiteDepartmentCostcenter

# 🟢 level4
from .levels.level4.employee_asset_project_site_role import EmployeeAssetProjectSiteRole
from .levels.level4.employee_training_certification_project_site import EmployeeTrainingCertificationProjectSite
from .levels.level4.tenant_site_department_cost_center_policy import TenantSiteDepartmentCostcenterPolicy
