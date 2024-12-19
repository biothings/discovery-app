# Use the latest Ubuntu image
FROM ubuntu:latest

# Install system dependencies
RUN apt update -o Acquire::Check-Date=false && \
    apt upgrade -y && \
    apt install -y libcurl4-openssl-dev libssl-dev build-essential python3 python3-pip vim git

# Clone the repository
RUN git clone https://github.com/biothings/discovery-app.git /discovery-app

# Create a virtual environment
RUN python3 -m venv /discovery-app/venv

# Activate the virtual environment and install Python dependencies
RUN /discovery-app/venv/bin/pip install --upgrade pip && \
    /discovery-app/venv/bin/pip install -r /discovery-app/requirements.txt

# Set environment variables for the virtual environment
ENV PATH="/discovery-app/venv/bin:$PATH"

# Set the working directory
WORKDIR /discovery-app

# Expose the API and Elasticsearch ports
EXPOSE 8000
EXPOSE 9200

# Start with a bash shell for interactive use
CMD ["/bin/bash"]
