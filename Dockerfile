# Use a base image with a Linux distribution of your choice (e.g., Ubuntu)
FROM python:3.7-slim-buster


# Update the package list and install necessary packages
RUN apt-get update && apt-get install -y \
    can-utils \
    python3 \
    python3-pip \
    python3-tk 

# Copy your program files into the Docker container
COPY . /usr/src/app

# Set the working directory
WORKDIR /usr/src/app

# RUN pip install -r requirements.txt

# Expose any necessary ports (optional)
# EXPOSE 80

# Specify the command to run your program
CMD ["python3", "tk_controller.py"]
