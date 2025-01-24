# Start with an official Python base image
FROM python:3.9-slim

# Set the working directory inside the container to '/app'
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project, but only the necessary files (e.g., the 'api' folder)
COPY ./api /app/api

# Set the entry point to run your app (the main file inside 'api' folder)
CMD ["python", "api/app.py"]
