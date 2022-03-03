FROM python:3.9-alpine

COPY ./requirement.txt /requirement.txt

RUN pip install -r requirements.txt

COPY ./main.py /usr/auto/main.py
COPY ./config.json /usr/auto/config.json
COPY ./exception /usr/auto/exception
COPY ./ocr_module /usr/auto/ocr_module
COPY ./send_module /usr/auto/send_module
COPY ./crypt_module /usr/auto/crypt_module

RUN echo "00 08 * * 3 cd /usr/auto && python3 main.py >> crontab.log 2>&1" > /var/spool/cron/crontabs/root
RUN crond