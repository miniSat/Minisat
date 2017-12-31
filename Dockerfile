FROM python:alpine

WORKDIR /minisat

ADD minisat/ /minisat

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python","manage.py","runserver"]

