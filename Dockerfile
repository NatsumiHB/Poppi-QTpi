FROM python:3-alpine
COPY ./src /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./main.py