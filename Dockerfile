FROM python:3.8
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN pip install -r requirements.txt
EXPOSE 5000
WORKDIR ./src/
CMD python ./main.py