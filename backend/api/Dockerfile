# Use the official Python base image
FROM python:3.10

# Copy .env file to the container

# Copy the requirements file to the container
COPY ./app/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code to the container
COPY ./app /app

# Expose the port on which the app will run
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]