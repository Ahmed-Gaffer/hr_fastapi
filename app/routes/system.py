# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi\app\routes\system.py
# File Name: system.py
# -----------------------------------------

from fastapi import APIRouter

router = APIRouter(tags=["system"])

@router.get("/health")
def health():
    return {"status": "ok"}
