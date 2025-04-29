FROM alpine:latest

RUN mkdir -p /app

RUN apk update && \
    apk add openjdk21 python3 py3-requests git cmake build-base zip unzip

RUN wget https://github.com/opentripplanner/OpenTripPlanner/releases/download/v2.7.0/otp-shaded-2.7.0.jar -O /app/otp.jar

RUN wget https://github.com/openstreetmap/osmosis/releases/download/0.49.2/osmosis-0.49.2.zip && \
    unzip osmosis-0.49.2.zip -d /opt && \
    mv /opt/osmosis-0.49.2 /opt/osmosis && \
    ln -s /opt/osmosis/bin/osmosis /usr/local/bin/osmosis

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --no-cache s5cmd

RUN git clone https://github.com/ad-freiburg/pfaedle && \
    cd pfaedle && \
    mkdir build && \
	cd build && \
	cmake .. && \
	make -j && \
	pwd && \
	make install

COPY tasks.sh /app/tasks.sh
COPY prepare_gtfs.py /app/prepare_gtfs.py
COPY IDFM.py /app/IDFM.py

RUN chmod +x /app/tasks.sh

WORKDIR /app

CMD ./tasks.sh
