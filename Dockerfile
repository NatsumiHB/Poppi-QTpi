FROM python:3-alpine
WORKDIR /srv/
RUN git clone https://github.com/NatsumiHB/Poppi-QTpi
WORKDIR /srv/Poppi-QTpi/
RUN chmod +x ./src/main.py
RUN pip install -r requirements.txt
CMD ./src/main.py