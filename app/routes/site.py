# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/routes\site.py
# File Name: site.py
# -----------------------------------------



# app/routes/sites.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.dependencies.dependencies import get_current_tenant
from app.models.site import Site, SiteCreate, SiteUpdate

router = APIRouter(prefix="/sites", tags=["Sites"])

# 🟢 عرض كل المواقع الخاصة بالشركة الحالية
@router.get("/")
def get_sites(
    session: Session = Depends(get_session),
    tenant=Depends(get_current_tenant),
):
    sites = session.exec(select(Site).where(Site.tenant_id == tenant.id)).all()
    return sites

# 🟢 عرض موقع واحد بالـ id
@router.get("/{site_id}")
def get_site(site_id: int, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

# 🟢 إضافة موقع جديد
@router.post("/")
def create_site(site_data: SiteCreate, session: Session = Depends(get_session)):
    site = Site.from_orm(site_data)
    session.add(site)
    session.commit()
    session.refresh(site)
    return site

# 🟢 تعديل بيانات موقع
@router.put("/{site_id}")
def update_site(site_id: int, site_data: SiteUpdate, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # تحديث الحقول لو اتبعت
    if site_data.name is not None:
        site.name = site_data.name
    if site_data.location is not None:
        site.location = site_data.location
    if site_data.tenant_id is not None:
        site.tenant_id = site_data.tenant_id

    session.commit()
    session.refresh(site)
    return site

# 🟢 حذف موقع
@router.delete("/{site_id}")
def delete_site(site_id: int, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    session.delete(site)
    session.commit()
    return {"detail": "Site deleted successfully"}