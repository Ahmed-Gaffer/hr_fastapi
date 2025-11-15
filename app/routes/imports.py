
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.import_excel import import_employees_from_excel

router = APIRouter()
# مسار استيراد الموظفين
@router.post("/import-employees")
def import_employees_endpoint():
    import_employees_from_excel("data/employees.xlsx")
    return JSONResponse({"message": "تم الاستيراد بنجاح"})