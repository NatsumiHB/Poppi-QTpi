FROM python:3.9-slim
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/

RUN apt-get update
RUN apt-get upgrade
RUN apt-get base-devel
RUN pip install -r requirements.txt

EXPOSE 5000
WORKDIR /srv/poppi/src/
CMD python ./main.py