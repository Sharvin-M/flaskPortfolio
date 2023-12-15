FROM python:3.11-stretch

WORKDIR /app

ADD . /app/

RUN pip3 install -r requirements.txt

CMD ["uswgi", "app.ini"]