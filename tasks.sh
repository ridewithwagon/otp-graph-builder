set -e

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/streetGraph.otp2.7.0.obj -O streetGraph.obj

python3 prepare_gtfs.py

wget https://download.geofabrik.de/europe/cyprus-latest.osm.pbf
osmosis \
  --read-pbf cyprus-latest.osm.pbf \
  --write-xml cyprus-latest.osm.xml
pfaedle -x cyprus-latest.osm.xml cy-kas
zip -r cy-kas.zip gtfs-out/
s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./cy-kas.zip "s3://${AWS_S3_BUCKET}/cy-kas.zip"
rm -rf cy-kas/
mv gtfs-out cy-kas

wget https://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf
osmosis \
  --read-pbf ile-de-france-latest.osm.pbf \
  --write-xml ile-de-france-latest.osm.xml
pfaedle -x ile-de-france-latest.osm.xml fr-idf
zip -r fr-idf.zip gtfs-out/
s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./fr-idf.zip "s3://${AWS_S3_BUCKET}/fr-idf.zip"
rm -rf fr-idf/
mv gtfs-out fr-idf

java -Xmx18G -jar otp.jar --loadStreet --save .

mkdir -p external
cp ./graph.obj ./external/graph.obj

s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./graph.obj "s3://${AWS_S3_BUCKET}/graph.otp2.7.0.obj"