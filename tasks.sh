set -e

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/streetGraph.otp2.7.0.obj -O streetGraph.obj

python3 prepare_gtfs.py

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/cyprus-latest.osm.bz2
bunzip2 cyprus-latest.osm.bz2
pfaedle -x cyprus-latest.osm cy-kas
cp gtfs-out/trips.txt cy-kas/
cp gtfs-out/stop_times.txt cy-kas/
cp gtfs-out/shapes.txt cy-kas/
cd cy-kas && zip -r ../cy-kas.zip . && cd ..
s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./cy-kas.zip "s3://${AWS_S3_BUCKET}/cy-kas.zip"

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/ile-de-france-latest.osm.bz2
bunzip2 ile-de-france-latest.osm.bz2
pfaedle -m bus -x ile-de-france-latest.osm fr-idf
cp gtfs-out/trips.txt fr-idf/
cp gtfs-out/stop_times.txt fr-idf/
cp gtfs-out/shapes.txt fr-idf/
cd fr-idf && zip -r ../fr-idf.zip . && cd ..
s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./fr-idf.zip "s3://${AWS_S3_BUCKET}/fr-idf.zip"

java $JAVA_HEAP_OPTS -jar otp.jar --loadStreet --save .

mkdir -p external
cp ./graph.obj ./external/graph.obj

s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./graph.obj "s3://${AWS_S3_BUCKET}/graph.otp2.7.0.obj"