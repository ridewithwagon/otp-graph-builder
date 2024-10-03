FROM alpine:latest

RUN apk update && \
    apk add openjdk21 python3 py3-boto3 py3-pip py3-requests

RUN mkdir -p /app

RUN wget https://repo1.maven.org/maven2/org/opentripplanner/otp/2.5.0/otp-2.5.0-shaded.jar -O /app/otp-2.5.0-shaded.jar

COPY tasks.sh /app/tasks.sh
COPY upload.py /app/upload.py
COPY prepare_gtfs.py /app/prepare_gtfs.py
COPY prepare_osm.py /app/prepare_osm.py

RUN chmod +x /app/tasks.sh

WORKDIR /app

CMD ./tasks.sh
