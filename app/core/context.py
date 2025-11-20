from typing import Optional
from contextvars import ContextVar

# متغير context لتخزين tenant_id الحالي
tenant_context: ContextVar[Optional[int]] = ContextVar('tenant_id', default=None)

def get_current_tenant() -> Optional[int]:
    """احصل على tenant_id الحالي"""
    return tenant_context.get()

def set_current_tenant(tenant_id: int):
    """اضبط tenant_id الحالي"""
    tenant_context.set(tenant_id)