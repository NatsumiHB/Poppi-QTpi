FROM python:3.8
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN pip install pipenv
RUN pipenv install
EXPOSE 5000
CMD pipenv run python ./src/main.py