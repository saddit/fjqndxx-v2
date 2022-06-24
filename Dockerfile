FROM python:3.9.13-bullseye
# FROM python:3.9-alpine

# run on evety Monday,Tuesday at 9:00
ENV CRONTIME="0 9 * * 1,4"
ENV username=
ENV password=
ENV pubKey=A7E74D2B6282AEB1C5EA3C28D25660A7
# ocr：baidu_image, tesseract
ENV ocrType=
ENV ocrSecret=
ENV ocrKey=
# bark, plus-plus, server_chan
ENV sendType=
ENV sendKey=
# success, fail, both
ENV sendMode=
ENV extUsers=
ENV TZ=Asia/Shanghai


RUN apt update && apt install -y cron tesseract-ocr libtesseract-dev libleptonica-dev

ADD ./ /root/tk-auto-study/ 
RUN cd /root/tk-auto-study && pip install -r requirements.txt

RUN crontab -l | { cat; echo "$CRONTIME python /root/tk-auto-study/docker.py"; } | crontab -;

CMD ["cron", "-f"]
