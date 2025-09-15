# Use a lightweight official Python base image
FROM python:3.12-slim  

# Set the working directory inside the container to /app
WORKDIR /app  

# Environment settings:
# - PYTHONDONTWRITEBYTECODE=1 → prevents Python from writing .pyc files
# - PYTHONUNBUFFERED=1 → makes Python output show up immediately (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1  

# Copy the requirements file first (so pip install layer can be cached)
COPY requirements.txt .  

# Install dependencies listed in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt  

# Copy the rest of your project code into the container
COPY . .  

# Set the default command: run your app (replace with your entry point)
CMD ["python", "main.py"]
