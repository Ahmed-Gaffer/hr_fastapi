# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\imports\employees.py
# File Name: employees.py
# -----------------------------------------

from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlmodel import Session
from app.database import get_session
from app.services.imports.employees import EmployeeImporter

router = APIRouter()

@router.post("/employees/")
async def employees_import(
    file: UploadFile = File(...),
    commit: bool = Query(False),
    allow_create_tenant: bool = Query(True),
    session: Session = Depends(get_session)
):
    """
    استيراد موظفين من ملف Excel واحد.
    الأعمدة المقترحة: code, name, department, company_name
    """
    stream = await file.read()
    importer = EmployeeImporter()
    report = importer.run(
        session=session,
        stream=stream,
        commit=commit,
        allow_create_tenant=allow_create_tenant
    )
    return report
