wget https://transport.data.gouv.fr/resources/79642/download -O rla.gtfs.zip
wget https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip -O idfm.gtfs.zip

wget http://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf
wget https://cdn1.arno.cl/2024%2F05%2Fnice.osm.pbf

java -jar otp-2.5.0-shaded.jar --build --save .

python3 upload.py