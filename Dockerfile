FROM python:3
COPY ./ /srv/poppi/
WORKDIR /srv/poppi/
RUN pip install -r requirements.txt
RUN pipenv install -r Pipfile
CMD pipenv run python ./src/main.py