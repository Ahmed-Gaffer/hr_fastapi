# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/models\employee.py
# File Name: employee.py
# -----------------------------------------



from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# 🟢 Enums علشان تمنع إدخال قيم عشوائية
class WorkStatus(str, Enum):
    ACTIVE = "يعمل"
    LEAVE = "اجازة بدون مرتب"
    STOPPED = "موقوف"


class InsuranceStatus(str, Enum):
    INSURED = "مؤمن"
    NOT_iNSURED = "غير مؤمن"


class EmployeeStatus(str, Enum):
    ACTIVE = "نشط"
    SUSPENDED = "موقوف"
    TERMINATED = "منتهي"


# 🧑 موديل الموظف
class Employee(SQLModel, table=True):
    """الموظف"""
    __tablename__ = "employee"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 🔗 علاقات أساسية
    tenant_id: int = Field(foreign_key="tenant.id", index=True)  # الشركة
    site_id: Optional[int] = Field(foreign_key="site.id", index=True)  # الموقع
    cost_center_id: Optional[int] = Field(foreign_key="cost_center.id", index=True)  # مركز التكلفة
    department_id: Optional[int] = Field(default=None, foreign_key="department.id", index=True)  # القسم

    # 🧑 بيانات أساسية
    code: str = Field(index=True)  # كود الموظف
    name: str  # اسم الموظف
    national_id: Optional[str] = None  # الرقم القومي
    job_title: Optional[str] = None  # الوظيفة
    hire_date: Optional[date] = None  # تاريخ التعيين

    # 💰 بيانات مالية
    base_salary: float = 0.0
    employee_category: Optional[str] = None  # فئة الموظف

    # 🏥 بيانات التأمين
    insurance_status: Optional[InsuranceStatus] = None

    # 📌 حالة العمل
    work_status: Optional[WorkStatus] = None
    status: EmployeeStatus = EmployeeStatus.ACTIVE

    # 🕒 تتبع
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔗 علاقات ORM
    tenant: "Tenant" = Relationship(back_populates="employees")
    site: Optional["Site"] = Relationship(back_populates="employees")
    cost_center: Optional["CostCenter"] = Relationship(back_populates="employees")
    department: Optional["Department"] = Relationship(back_populates="employees")

    attendances: List["Attendance"] = Relationship(back_populates="employee")
    salaries: List["Salary"] = Relationship(back_populates="employee")
    details: Optional["EmployeeDetails"] = Relationship(back_populates="employee")
    trainings: List["EmployeeTraining"] = Relationship(back_populates="employee")


# 🟢 موديلات Create / Update
class EmployeeCreate(SQLModel):
    code: str
    name: str
    base_salary: float
    national_id: Optional[str] = None
    job_title: Optional[str] = None
    hire_date: Optional[date] = None
    tenant_id: Optional[int] = None
    site_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    department_id: Optional[int] = None
    insurance_status: Optional[InsuranceStatus] = None
    employee_category: Optional[str] = None
    work_status: Optional[WorkStatus] = None
    status: Optional[EmployeeStatus] = None


class EmployeeUpdate(SQLModel):
    code: Optional[str] = None
    name: Optional[str] = None
    base_salary: Optional[float] = None
    national_id: Optional[str] = None
    job_title: Optional[str] = None
    hire_date: Optional[date] = None
    tenant_id: Optional[int] = None
    site_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    department_id: Optional[int] = None
    insurance_status: Optional[InsuranceStatus] = None
    employee_category: Optional[str] = None
    work_status: Optional[WorkStatus] = None
    status: Optional[EmployeeStatus] = None