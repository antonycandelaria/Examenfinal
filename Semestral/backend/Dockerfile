# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias para instalar primero las dependencias
COPY requirements.txt /app/requirements.txt

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del backend al contenedor
COPY . /app

# Expone el puerto que Flask usará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]


