FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
