# Python 3.10 slim tabanlı imaj kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılık dosyasını ve Python kodunu kopyala
COPY requirements.txt .
COPY crawler.py .

# Virtual Environment oluştur
RUN python -m venv /app/venv

# Virtual Environment içinde pip'i güncelle ve bağımlılıkları yükle
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# Virtual Environment ile Python kodunu çalıştır
CMD ["/app/venv/bin/python", "crawler.py"]
