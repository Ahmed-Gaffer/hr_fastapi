from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from io import BytesIO
from sqlmodel import Session
from app.database import get_session
from app.models.tenant import Tenant
from app.dependencies import get_current_tenant
import traceback

# استخدم الadapter الجديد
from app.services.importer import Importer

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/bulk")
async def bulk_import(
    file: UploadFile = File(...),
    commit: bool = Query(True, description="إذا false يكون dry-run ولا يكتب في DB"),
    session: Session = Depends(get_session),
    tenant: Tenant = Depends(get_current_tenant)
):
    data = await file.read()
    stream = BytesIO(data)
    importer = Importer(session=session, tenant=tenant)
    try:
        filename = file.filename.lower()
        if "employee" in filename:
            result = importer.import_employees(stream, commit=commit)
        elif "salary" in filename:
            result = importer.import_salaries(stream, commit=commit)
        else:
            result = {"status": "failed", "errors": ["نوع ملف غير مدعوم"]}
        return JSONResponse(content={"status": "ok", **result})
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    