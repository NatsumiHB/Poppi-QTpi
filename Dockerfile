FROM python:3-alpine
CMD mkdir /app
WORKDIR /app
CMD git clone https://github.com/NatsumiHB/Poppi-QTpi
CMD chmod +x ./src/main.py
RUN pip install -r requirements.txt
CMD python ./src/main.py