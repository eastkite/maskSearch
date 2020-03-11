FROM ubuntu:18.04
FROM python:3.8
FROM ubuntu:18.04

MAINTAINER eastkite eastkite13@gmail.com

RUN apt-get update -y
RUN apt-get install nano

# 한글 설치 
RUN apt-get install -y locales locales-all

ENV LC_ALL ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANG ko_KR.EUC-KR
ENV LANGUAGE ko_KR:ko:en_GB:en

# RUN apt-get install language-pack-ko -y
# RUN apt-get install language-pack-ko-base -y

COPY . /Users/baedy/Documents/seorin/docker
WORKDIR /Users/baedy/Documents/seorin/docker

# pip3 설치 
RUN apt-get install -y python3-pip python-dev build-essential
# RUN apt-get install -y software-properties-common

# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt-get update

# RUN apt-get install python3.8 -y
# RUN apt-get upgrade python3

# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
# RUN update-alternatives --config python3
# RUN apt-get install python3-pip -y

RUN pip3 install -r requirements.txt

# git 설치
RUN apt-get install git -y

# ssh-keygen 관련 설정
ARG SSH_KEY

RUN mkdir -p /root/.ssh/ && \
    echo "$SSH_KEY" > /root/.ssh/id_rsa && \
    chmod -R 600 /root/.ssh/ && \
    ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

RUN git clone git@github.com:eastkite/maskSearch.git

RUN cp firstStart.sh ./Hotdeal-Crawling-Server/

EXPOSE 8090:8090


