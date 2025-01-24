# Start with an official Python base image
FROM python:3.9-slim

# Set the working directory inside the container to '/app'
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 5000 for Flask app
EXPOSE 5000

# Set the command to run the app
CMD ["python", "api/app.py"]
