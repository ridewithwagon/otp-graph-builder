wget https://transport.data.gouv.fr/resources/79642/download -O rla.gtfs.zip
wget https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip -O idfm.gtfs.zip

wget http://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf
wget http://download.geofabrik.de/europe/france/provence-alpes-cote-d-azur-latest.osm.pbf

java -jar otp-2.5.0-shaded.jar --build --save .

python3 upload.py