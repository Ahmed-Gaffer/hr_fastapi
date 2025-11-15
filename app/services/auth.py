# خدمات التوثيق باستخدام JWT
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# إعداد التشفير لكلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# مفتاح سري لتوقيع التوكن (غيّره في مشروعك الحقيقي)
SECRET_KEY = "secretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# دالة لتشفير كلمة المرور
def hash_password(password: str):
    return pwd_context.hash(password)

# دالة للتحقق من كلمة المرور
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# دالة لإنشاء توكن JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # نسخ البيانات
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # إضافة وقت الانتهاء
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
