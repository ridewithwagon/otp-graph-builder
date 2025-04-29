set -e

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/streetGraph.otp2.7.0.obj -O streetGraph.obj

python3 prepare_gtfs.py

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/cyprus-latest.osm.bz2
bunzip2 cyprus-latest.osm.bz2
pfaedle -x cyprus-latest.osm cy-kas
zip -r cy-kas.zip gtfs-out/
s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./cy-kas.zip "s3://${AWS_S3_BUCKET}/cy-kas.zip"
rm -rf cy-kas/
mv gtfs-out cy-kas

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/ile-de-france-latest.osm.bz2
bunzip2 ile-de-france-latest.osm.bz2
pfaedle -x ile-de-france-latest.osm fr-idf
zip -r fr-idf.zip gtfs-out/
s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./fr-idf.zip "s3://${AWS_S3_BUCKET}/fr-idf.zip"
rm -rf fr-idf/
mv gtfs-out fr-idf

java $JAVA_HEAP_OPTS -jar otp.jar --loadStreet --save .

mkdir -p external
cp ./graph.obj ./external/graph.obj

s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./graph.obj "s3://${AWS_S3_BUCKET}/graph.otp2.7.0.obj"