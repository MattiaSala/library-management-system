# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
