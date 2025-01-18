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

# Lanksčiam naudojimui lokaliai ir cloude - įvedame environment variables
# Čia parašomi defaultai, kuriuos galima overridinti leidžiant konteinerį
ENV AWS_ACCESS_KEY_ID=your_access_key_id
ENV AWS_SECRET_ACCESS_KEY=your_secret_access_key
ENV AWS_REGION=eu-central-1
ENV DYNAMODB_ENDPOINT=http://localhost:8000

# Atidarom portą, reikalingą API darbui
EXPOSE 5000

# Nustatom kokia komanda paleis appsą
CMD ["python", "main_app.py"]