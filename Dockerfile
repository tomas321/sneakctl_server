FROM python:3.6
ENV PROJECT_DIR=/opt/sneakctl_server/

WORKDIR $PROJECT_DIR

COPY . $PROJECT_DIR

RUN apt update &&\
    apt upgrade -y &&\
    apt install -y libdbus-1-dev &&\
    pip3 install -r requirements.txt

ENTRYPOINT ["./docker/docker-entrypoint.sh"]
