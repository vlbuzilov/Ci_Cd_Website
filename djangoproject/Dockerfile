# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /djangoproject

COPY /requirements.txt /djangoproject/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /djangoproject/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start uWSGI
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
