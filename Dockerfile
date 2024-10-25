# Use the official Python 3.10 image
FROM python:3.11

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory in the container
WORKDIR /flaskapp

# Copy the entire app directory into the container working directory
COPY . /flaskapp

ENV FLASK_DEBUG="development"

RUN pip3 install -r requirements.txt
EXPOSE 8080

CMD ["python3", "app.py", "run", "--host=0.0.0.0", "--port=8080"]
