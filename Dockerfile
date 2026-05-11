# استخدام نسخة بايثون خفيفة ومستقرة (Debian-based) كما تحب
FROM python:3.10-slim

# إعداد مجلد العمل داخل السيرفر
WORKDIR /code

# نسخ ملف المتطلبات أولاً لتسريع عملية الـ Build
COPY ./requirements.txt /code/requirements.txt

# تثبيت المكتبات
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# نسخ باقي ملفات المشروع (بما فيها ملفات الإكسيل و قاعدة البيانات)
COPY . .

# إنشاء مستخدم غير "root" للأمان (Hugging Face يفضل ذلك)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# تشغيل التطبيق باستخدام uvicorn
# ملاحظة: Hugging Face يستخدم بورت 7860 افتراضياً
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]