# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port Flask will run on
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]