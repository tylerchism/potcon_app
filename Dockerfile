# using ubuntu as base image
FROM ubuntu:20.04
ENV TZ=America
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#update and install dependencies
RUN mkdir -p /home

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3-pip && python3 -m pip install -U pip
RUN apt-get install -y ca-certificates wget tar ssh gcc g++ make zlib1g-dev python3 python3-numpy git tree cmake
RUN apt-get install libboost-all-dev -y
RUN apt install libtbb-dev -y
RUN apt install nodejs -y
RUN apt install npm -y

COPY tylerinstall.sh /home/tylerinstall.sh
RUN /home/tylerinstall.sh
COPY requirements.txt /home
RUN python3 -m pip install -r /home/requirements.txt

COPY script /home/script
WORKDIR /home

CMD python3 /home/script/runtimejob.py -c -r && cd /opt/potree && npm start


