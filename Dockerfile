# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el proyecto
COPY . .

# Expone el puerto (por defecto 8000)
EXPOSE 8000

# Comando de inicio (Channels + Uvicorn)
CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000"]