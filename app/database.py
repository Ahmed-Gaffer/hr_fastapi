# استيراد الأدوات الخاصة بإنشاء الجداول والاتصال بقاعدة البيانات
from sqlmodel import SQLModel, create_engine

# استيراد رابط قاعدة البيانات من ملف الإعدادات
from app.core.config import DATABASE_URL

# إنشاء محرك الاتصال بقاعدة البيانات
# echo=True معناها إظهار أوامر SQL في الكونسول أثناء التشغيل
engine = create_engine(DATABASE_URL, echo=True)

# دالة لإنشاء الجداول عند بدء التشغيل
def create_db_and_tables():
    # هذه الدالة تنشئ كل الجداول المعرفة باستخدام SQLModel
    SQLModel.metadata.create_all(engine)
