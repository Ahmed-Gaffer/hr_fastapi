# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\imports\salaries.py
# File Name: salaries.py
# -----------------------------------------

from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlmodel import Session
from app.database import get_session
from app.models.tenant import Tenant
from app.services.imports.salaries import SalaryImporter

router = APIRouter()

@router.post("/salaries/")
async def salaries_import(
    file: UploadFile = File(...),
    commit: bool = Query(False),
    allow_create_employee: bool = Query(True),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends()
):
    stream = await file.read()
    importer = SalaryImporter()
    report = importer.run(
        session,
        tenant,
        stream,
        commit=commit,
        allow_create_employee=allow_create_employee
    )
    return report
