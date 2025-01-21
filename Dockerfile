# Pasirnekamas lengvas pythono image
FROM python:3.10-slim

# Nustatoma darbinė direktorija konteineryje
WORKDIR /app

# Nukopijuojamas requirements failas
COPY requirements.txt /app/

# Instaliuojam reikalingus dalykus, nurodytus requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Nukopijuojam pačios aplikacijos kodą į konteinerį
COPY . /app/

# Atidarom portą, reikalingą API darbui
EXPOSE 5000

# Nustatom kokia komanda paleis appsą
CMD ["python", "main_app.py"]
