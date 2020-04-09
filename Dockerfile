FROM gorialis/discord.py:3.8.1-alpine-master-full
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN apk add build-base
RUN pip install -r requirements.txt
CMD python ./src/main.py
