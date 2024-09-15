wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C6_google_transit.zip&rel=True" -O ./cy-006.zip
unzip cy-006.zip -d cy-006
rm cy-006/fare_rules.txt
rm cy-006/fare_attributes.txt

wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C2_google_transit.zip&rel=True" -O ./cy-002.zip

wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C4_google_transit.zip&rel=True" -O ./cy-004.zip
unzip cy-004.zip -d cy-004
rm cy-004/fare_rules.txt
rm cy-004/fare_attributes.txt

wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C5_google_transit.zip&rel=True" -O ./cy-005.zip
wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C9_google_transit.zip&rel=True" -O ./cy-009.zip
wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C10_google_transit.zip&rel=True" -O ./cy-010.zip
wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C11_google_transit.zip&rel=True" -O ./cy-011.zip
wget "https://transport.data.gouv.fr/resources/79642/download" -O ./fr-rla.zip
wget "https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/" -O ./fr-tou.zip

java -Xmx4G -jar otp-2.5.0-shaded.jar --build --save .

python3 upload.py