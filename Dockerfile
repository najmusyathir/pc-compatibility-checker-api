# Creating project in Docker
#1. Prepare your project [eg: FastAPI]

#2. Create "Dockerfile": Refer codes below

#3.  Run batch in project file with this
# >> docker build -t fastapi .
# Note: run on Powershell, cd to where Docker file is located, then WALLA!! Your docker image is created



# Start with a Python base image
FROM python:3.11

# Set the working directory within the container
WORKDIR /app

# Copy the app package and package-lock.json file into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose the port that your FastAPI application will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


#Push Docker image to Docker Hub

# 1. put tag(the version of the system) and rename it with 
# Run:  docker tag created_image_name your_username/your_wanted_image_name:v
# Example: docker tag pc-compatibility-checker-api najmusyathir/pc-compatibility-checker-api:v1.0

# 2. Login into your docker, can be login early in Docker website/software
# Run : docker login

# 3. Push your created docker image
# Run : docker push your_created_docker_name
# Example: najmusyathir/pc-compatibility-checker-api:v1.0
#
# !! Done !!
# Extras:
# Run: Docker images >> to list all your docker available

