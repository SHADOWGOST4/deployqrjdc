FROM python:3.9

WORKDIR /app

# 1. Copia solo requirements.txt y lo instala.
# Esto es bueno para el cache de Docker: si requirements.txt no cambia,
# esta capa no se reconstruye en builds posteriores.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copia el resto del código de la aplicación.
# manage.py y el resto de tu proyecto se copiarán a /app
COPY . .

# 3. El comando para ejecutar.
# WORKDIR sigue siendo /app, y manage.py estará en /app/manage.py.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
