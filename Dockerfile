# Gunakan base image Python
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Jalankan migrasi saat build
RUN python manage.py migrate

# Expose port 8000
EXPOSE 8000

# Jalankan server Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djproject.wsgi"]