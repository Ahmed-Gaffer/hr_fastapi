from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Employee(SQLModel, table=True):
    """الموظف"""
    id: Optional[int] = Field(default=None, primary_key=True)

    # ربط بالشركة (Tenant)
    tenant_id: int = Field(index=True)

    # بيانات أساسية
    code: str = Field(index=True)                # كود الموظف
    name: str                                   # اسم الموظف
    national_id: Optional[str] = None           # الرقم القومي
    job_title: Optional[str] = None             # الوظيفة
    hire_date: Optional[datetime] = None        # تاريخ التعيين

    # بيانات الشركة والموقع
    company_name: Optional[str] = None          # اسم الشركة
    site_name: Optional[str] = None             # اسم الموقع
    cost_center: Optional[str] = None           # مركز التكلفة

    # بيانات إضافية
    insurance_status: Optional[str] = None      # حالة التأمين (نعم / لا)
    employee_category: Optional[str] = None     # فئة الموظف
    work_status: Optional[str] = None           # يعمل / اجازة بدون مرتب / لا يعمل

    # المرتب والحالة
    base_salary: float = 0.0
    status: str = "نشط"                         # الحالة العامة (نشط / موقوف / إلخ)
    department: Optional[str] = None            # القسم

    # تتبع
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
class EmployeeCreate(SQLModel):
    code: str
    name: str
    base_salary: float
    national_id: Optional[str] = None
    job_title: Optional[str] = None
    hire_date: Optional[datetime] = None
    company_name: Optional[str] = None
    site_name: Optional[str] = None
    cost_center: Optional[str] = None
    insurance_status: Optional[str] = None
    employee_category: Optional[str] = None
    work_status: Optional[str] = None
    status: Optional[str] = None
    department: Optional[str] = None


class EmployeeUpdate(SQLModel):
    code: Optional[str] = None
    name: Optional[str] = None
    base_salary: Optional[float] = None
    national_id: Optional[str] = None
    job_title: Optional[str] = None
    hire_date: Optional[datetime] = None
    company_name: Optional[str] = None
    site_name: Optional[str] = None
    cost_center: Optional[str] = None
    insurance_status: Optional[str] = None
    employee_category: Optional[str] = None
    work_status: Optional[str] = None
    status: Optional[str] = None
    department: Optional[str] = None