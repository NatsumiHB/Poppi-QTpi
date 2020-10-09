FROM python:3.9-slim
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/

RUN sudo apt-get update
RUN sudo apt-get upgrade
RUN sudo apt-get base-devel
RUN pip install -r requirements.txt

EXPOSE 5000
WORKDIR /srv/poppi/src/
CMD python ./main.py