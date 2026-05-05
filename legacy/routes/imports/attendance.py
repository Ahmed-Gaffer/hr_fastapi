# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\imports\attendance.py
# File Name: attendance.py
# -----------------------------------------



from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlmodel import Session
from app.database import get_session
from app.models.tenant import Tenant
from app.services.imports.attendance import AttendanceImporter

router = APIRouter()

@router.post("/attendance/")
async def attendance_import(
    file: UploadFile = File(...),
    commit: bool = Query(False),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends()
):
    stream = await file.read()
    importer = AttendanceImporter()
    report = importer.run(session, tenant, stream, commit=commit)
    return report