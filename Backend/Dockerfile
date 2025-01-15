FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker caching
COPY requirements.txt /app/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Now copy the rest of the application files
COPY . /app

# Expose port 8001 for the Django app
EXPOSE 8001

# Start the Django development server on port 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
