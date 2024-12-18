FROM ubuntu:latest

# Install dependencies including python3-venv
RUN apt update -o Acquire::Check-Date=false && \
    apt upgrade -y && \
    apt install -y libcurl4-openssl-dev libssl-dev build-essential python3 python3-pip vim git && \
    # git clone https://github.com/biothings/discovery-app.git && \
    # pip3 install -r /discovery-app/requirements.txt

# Clone the repository
RUN git clone https://github.com/biothings/discovery-app.git /discovery-app

# Create a virtual environment
RUN python3 -m venv /discovery-app/venv

# Activate the virtual environment and install requirements
RUN /discovery-app/venv/bin/pip install --upgrade pip && \
    /discovery-app/venv/bin/pip install -r /discovery-app/requirements.txt

# Copy the JSON file into the container
# COPY ./data/your_data.json /discovery-app/data/your_data.json

# Set environment variables
ENV PATH="/discovery-app/venv/bin:$PATH"
# WORKDIR /discovery-app

# Expose port
EXPOSE 8000

# Automatically restore data into Elasticsearch and then start the app``
# Expect the JSON file to be provided via a volume
CMD ["python3", "-c", "from discovery.utils.backup import restore_from_file; restore_from_file('/discovery-app/tests/data/dde_backup_20230815.json'); import index; index.main()"]

# COPY ./config_key.py /discovery-app/config_key.py
# WORKDIR /discovery-app
# EXPOSE 8000

# RUN git pull
# ENTRYPOINT ["python3", "index.py", "--debug"]
