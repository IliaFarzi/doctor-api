# 1. استفاده از تصویر پایه پایتون
FROM python:3.11-slim

# 2. تنظیم دایرکتوری کاری
WORKDIR /app

# 3. کپی فایل‌های پروژه به کانتینر
COPY . /app

# 4. نصب پکیج‌های مورد نیاز
RUN pip install --no-cache-dir fastapi uvicorn pymongo pydantic

# 5. باز کردن پورت اپلیکیشن
EXPOSE 8000

# 6. اجرای اپلیکیشن با uvicorn
CMD ["uvicorn", "appointment:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
