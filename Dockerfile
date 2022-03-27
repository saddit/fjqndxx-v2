FROM python:3.7.13-alpine

# run on evety Monday,Tuesday at 9:00
ENV CRONTIME="0 9 * * 1,4"
ENV username=
ENV password=
ENV pubKey=A7E74D2B6282AEB1C5EA3C28D25660A7
# bark, plus-plus, server_chan
ENV sendType=
ENV sendKey=
# success, fail, both
ENV sendMode=
ENV extUsers=

RUN apk update; \
    apk add git gcc libc-dev libxml2-dev libxslt-dev;

RUN git clone https://github.com/838239178/tk-auto-study.git /root/tk-auto-study \
    && cd /root/tk-auto-study \
    && git checkout master; \
    pip install -r requirements.txt;

RUN crontab -l | { cat; echo "$CRONTIME python /root/tk-auto-study/docker.py"; } | crontab -; \
    crond -b -l 8;

CMD ["tail", "-f", "/dev/null"]