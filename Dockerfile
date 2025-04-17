FROM alpine:latest

RUN mkdir -p /app

RUN apk update && \
    apk add openjdk21 python3 py3-requests

RUN wget https://github.com/opentripplanner/OpenTripPlanner/releases/download/v2.7.0/otp-shaded-2.7.0.jar -O /app/otp.jar

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk add --no-cache s5cmd

COPY tasks.sh /app/tasks.sh
COPY prepare_gtfs.py /app/prepare_gtfs.py

RUN chmod +x /app/tasks.sh

WORKDIR /app

CMD ./tasks.sh
