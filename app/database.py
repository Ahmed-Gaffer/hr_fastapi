from sqlmodel import Session
from sqlmodel import SQLModel, create_engine        # استيراد الأدوات الخاصة بإنشاء الجداول والاتصال بقاعدة البيانات
from app.core.config import DATABASE_URL            # استيراد رابط قاعدة البيانات من ملف الإعدادات

engine = create_engine(DATABASE_URL, echo=True)     # إنشاء محرك الاتصال بقاعدة البيانات، echo=True معناها إظهار أوامر SQL في الكونسول أثناء التشغيل
def create_db_and_tables():                         # دالة لإنشاء الجداول عند بدء التشغيلSQLModel.metadata.create_all(engine)            # إنشاء كل الجداول المعرفة في الموديلات باستخدام الميتاداتا    # هذه الدالة تنشئ كل الجداول المعرفة باستخدام SQLModel
    SQLModel.metadata.create_all(engine)            # إنشاء كل الجداول المعرفة في الموديلات باستخدام الميتاداتا    # هذه الدالة تنشئ كل الجداول المعرفة باستخدام SQLModel

#دالة للحصول على جلسة قاعدة البيانات (مطلوبة في الراوترات)
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()