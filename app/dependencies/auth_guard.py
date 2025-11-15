# التحقق من التوكن وصلاحية المستخدم
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.services.auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# دالة لاستخراج بيانات المستخدم من التوكن
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(status_code=401, detail="توكن غير صالح")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="فشل التحقق من التوكن")

# دالة للتحقق إن المستخدم مدير فقط
def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="صلاحية غير كافية")
    return user
