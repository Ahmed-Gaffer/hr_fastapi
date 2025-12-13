# app/models/__init__.py
"""
Models package initializer
Explicit imports only – errors must surface immediately.
"""

# =========================
# Base / Core Models
# =========================
from .tenant import Tenant, TenantStatus
from .site import Site
from .project import Project
from .cost_center import CostCenter
from .department import Department

from .employee import (
    Employee,
    WorkStatus,
    InsuranceStatus,
    EmployeeStatus,
)

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
from .public_holiday import PublicHoliday
from .performance_review import PerformanceReview

# =========================
# Levels
# =========================

# ---- Level 1 ----
from .levels.level1.employee_advance_salary import EmployeeAdvanceSalary
from .levels.level1.employee_asset import EmployeeAsset
from .levels.level1.employee_attendance import EmployeeAttendance
from .levels.level1.employee_benefit import EmployeeBenefit
from .levels.level1.employee_certification import EmployeeCertification
from .levels.level1.employee_configuration import EmployeeConfiguration
from .levels.level1.employee_cost_center import EmployeeCostCenter
from .levels.level1.employee_department import EmployeeDepartment
from .levels.level1.employee_deduction import EmployeeDeduction
from .levels.level1.employee_disciplinary import EmployeeDisciplinary
from .levels.level1.employee_leave import EmployeeLeave, LeaveType
from .levels.level1.employee_loan import EmployeeLoan
from .levels.level1.employee_performance_review import EmployeePerformanceReview
from .levels.level1.employee_policy import EmployeePolicy
from .levels.level1.employee_project import EmployeeProject
from .levels.level1.employee_public_holiday import EmployeePublicHoliday
from .levels.level1.employee_reward import EmployeeReward
from .levels.level1.employee_role import EmployeeRole
from .levels.level1.employee_salary import EmployeeSalary
from .levels.level1.employee_skill import EmployeeSkill
from .levels.level1.employee_tenant import EmployeeTenant
from .levels.level1.employee_training import EmployeeTraining
from .levels.level1.employee_user import EmployeeUser

# ---- Level 2 ----
from .levels.level2.employee_asset_site import EmployeeAssetSite
from .levels.level2.employee_department_role import EmployeeDepartmentRole
from .levels.level2.employee_department_site import EmployeeDepartmentSite
from .levels.level2.employee_policy_cost_center import EmployeePolicyCostCenter
from .levels.level2.employee_project_cost_center import EmployeeProjectCostCenter
from .levels.level2.employee_project_site import EmployeeProjectSite
from .levels.level2.employee_site_role import EmployeeSiteRole
from .levels.level2.employee_training_certification import EmployeeTrainingCertification
from .levels.level2.project_department_policy import ProjectDepartmentPolicy
from .levels.level2.project_employee_role import ProjectEmployeeRole

# ---- Level 3 ----
from .levels.level3.employee_asset_project_site import EmployeeAssetProjectSite
from .levels.level3.employee_asset_site_role import EmployeeAssetSiteRole
from .levels.level3.employee_project_role_cost_center import EmployeeProjectRoleCostCenter
from .levels.level3.employee_project_site_cost_center import EmployeeProjectSiteCostCenter
from .levels.level3.employee_project_site_department import EmployeeProjectSiteDepartment
from .levels.level3.employee_training_certification_project import EmployeeTrainingCertificationProject
from .levels.level3.employee_training_project_site import EmployeeTrainingProjectSite
from .levels.level3.tenant_site_department_cost_center import TenantSiteDepartmentCostCenter

# ---- Level 4 ----
from .levels.level4.employee_asset_project_site_role import EmployeeAssetProjectSiteRole
from .levels.level4.employee_training_certification_project_site import EmployeeTrainingCertificationProjectSite
from .levels.level4.tenant_site_department_cost_center_policy import TenantSiteDepartmentCostCenterPolicy
