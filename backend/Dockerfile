# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

#RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY wsgi.py /app

# PORT
EXPOSE 5006

#RUN pip install gunicorn

# Command to run your application
CMD ["python", "/app/wsgi.py"]

#CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5005", "--timeout", "0", "--keep-alive", "0", "--preload", "wsgi:app"]



