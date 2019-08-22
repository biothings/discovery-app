FROM ubuntu

RUN apt update -o Acquire::Check-Date=false && \
    apt upgrade -y && \
    apt install -y libcurl4-openssl-dev libssl-dev build-essential python3 python3-pip vim git && \
    git clone https://github.com/biothings/discovery-app.git && \
    pip3 install -r /discovery-app/requirements.txt

COPY ./discovery/config_key.py /discovery-app/discovery/config_key.py
WORKDIR /discovery-app
EXPOSE 8000

RUN git pull
ENTRYPOINT ["python3", "discovery/index.py", "--debug"]