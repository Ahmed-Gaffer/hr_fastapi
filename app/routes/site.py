# app/routes/sites.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.site import Site

router = APIRouter(prefix="/sites", tags=["Sites"])

# عرض كل المواقع
@router.get("/")
def get_sites(session: Session = Depends(get_session)):
    sites = session.exec(select(Site)).all()
    return sites

# عرض موقع واحد بالـ id
@router.get("/{site_id}")
def get_site(site_id: int, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

# إضافة موقع جديد
@router.post("/")
def create_site(site: Site, session: Session = Depends(get_session)):
    session.add(site)
    session.commit()
    session.refresh(site)
    return site

# تعديل بيانات موقع
@router.put("/{site_id}")
def update_site(site_id: int, site_data: Site, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    site.name = site_data.name
    site.location = site_data.location
    site.company_name = site_data.company_name
    site.cost_center = site_data.cost_center
    session.add(site)
    session.commit()
    session.refresh(site)
    return site

# حذف موقع
@router.delete("/{site_id}")
def delete_site(site_id: int, session: Session = Depends(get_session)):
    site = session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    session.delete(site)
    session.commit()
    return {"detail": "Site deleted successfully"}
