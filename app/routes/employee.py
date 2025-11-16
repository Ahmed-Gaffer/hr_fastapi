# app/routes/employees.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.employee import Employee

router = APIRouter(prefix="/employees", tags=["Employees"])

# عرض كل الموظفين
@router.get("/")
def get_employees(session: Session = Depends(get_session)):
    employees = session.exec(select(Employee)).all()
    return employees

# عرض موظف واحد بالـ id
@router.get("/{employee_id}")
def get_employee(employee_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# إضافة موظف جديد
@router.post("/")
def create_employee(employee: Employee, session: Session = Depends(get_session)):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

# تعديل بيانات موظف
@router.put("/{employee_id}")
def update_employee(employee_id: int, employee_data: Employee, session: Session = Depends(get_session)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.name = employee_data.name
    employee.national_id = employee_data.national_id
    employee.old_code = employee_data.old_code
    employee.site_id = employee_data.site_id
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

# حذف موظف
@router.delete("/{employee_id}")
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    return {"detail": "Employee deleted successfully"}
