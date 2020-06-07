FROM python:3.8
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./src/main.py