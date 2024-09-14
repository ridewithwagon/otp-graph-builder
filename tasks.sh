wget "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C9_google_transit.zip&rel=True" -O ./cy-all.zip
wget "https://transport.data.gouv.fr/resources/79642/download" -O ./fr-rla.zip
wget "https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/" -O ./fr-tou.zip

java -Xmx4G -jar otp-2.5.0-shaded.jar --build --save .

python3 upload.py