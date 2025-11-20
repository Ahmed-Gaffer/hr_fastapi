from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlmodel import Session
from app.database import get_session
from app.services.bulk_importer_v3 import BulkImporterV3

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/bulk")
async def import_bulk(file: UploadFile = File(...), commit: bool = Query(False, description="commit=true لحفظ التغييرات، افتراضياً dry-run"), session: Session = Depends(get_session)):
    if not file.filename.lower().endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
        raise HTTPException(status_code=400, detail="الملف يجب أن يكون Excel (.xlsx/.xlsm)")
    contents = await file.read()
    importer = BulkImporterV3(contents, session)
    report = importer.import_file(commit=commit)
    # إذا فشل التحقق الأساسي - ارجع 400
    if report.get("status") == "failed":
        raise HTTPException(status_code=500, detail=report.get("error", "import failed"))
    return report