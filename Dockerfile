FROM python:3-alpine
WORKDIR /srv/
CMD git clone https://github.com/NatsumiHB/Poppi-QTpi
WORKDIR /srv/Poppi-QTpi/
CMD chmod +x ./src/main.py
RUN pip install -r requirements.txt
CMD ./src/main.py