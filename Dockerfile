FROM python:3.8-slim
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN pip install -r requirements.txt
EXPOSE 5000
WORKDIR /srv/poppi/src/
CMD python ./main.py