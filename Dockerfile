FROM python:3.9-alpine
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN apk add build-base
RUN pip install -r requirements.txt
CMD python ./src/main.py