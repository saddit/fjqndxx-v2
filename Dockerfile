FROM python:3.9-alpine

# run on evety Monday,Tuesday at 9:00
ENV CRONTIME="0 9 * * 1,4"
ENV username=
ENV password=
ENV pubKey=A7E74D2B6282AEB1C5EA3C28D25660A7
# ocr：baidu_image
ENV OCR_TYPE=
ENV OCR_SECRET_KEY=
ENV OCR_API_KEY=
# bark, plus-plus, server_chan
ENV sendType=
ENV sendKey=
# success, fail, both
ENV sendMode=
ENV extUsers=
ENV TZ=Asia/Shanghai

RUN apk update; \
    apk add tzdata git gcc libc-dev libxml2-dev libxslt-dev;

RUN cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone

RUN git clone https://github.com/838239178/tk-auto-study.git /root/tk-auto-study \
    && cd /root/tk-auto-study \
    && git checkout master; \
    pip install -r requirements.txt;

RUN crontab -l | { cat; echo "$CRONTIME python /root/tk-auto-study/docker.py"; } | crontab -; \
    crond -b -l 8;

CMD ["tail", "-f", "/dev/null"]