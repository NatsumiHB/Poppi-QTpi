FROM python:3-alpine
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN pip install -r requirements.txt
CMD python ./src/main.py