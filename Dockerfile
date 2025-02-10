# Selecting a lightweight Python image
FROM python:3.10-slim

# Stating the working directory inside the container
WORKDIR /app

# Copying the requirements file into the container
COPY requirements.txt /app/

# Installing dependencies listed in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copying the application code into the container
COPY . /app/

# Exposing the port required for communication with the database
EXPOSE 5000

# Stating the command that will launch the app
CMD ["python", "main_app.py"]
