FROM ubuntu

RUN apt update -o Acquire::Check-Date=false && \
    apt upgrade -y && \
    apt install -y libcurl4-openssl-dev libssl-dev build-essential python3 python3-pip vim git
RUN git clone https://github.com/biothings/discovery-app.git
RUN python3 -m venv /discovery-app/.venv && \
    /discovery-app/.venv/bin/pip install -r /discovery-app/requirements.txt


COPY ./config_key.py /discovery-app/config_key.py
WORKDIR /discovery-app
EXPOSE 8000

RUN git pull
ENTRYPOINT ["/discovery-app/.venv/bin/python", "index.py"]
