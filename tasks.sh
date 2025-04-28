set -e

wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/streetGraph.otp2.7.0.obj -O streetGraph.obj

python3 prepare_gtfs.py

java -Xmx18G -jar otp.jar --loadStreet --save .

mkdir -p external
cp ./graph.obj ./external/graph.obj

s5cmd --endpoint-url="${AWS_ENDPOINT_URL}" \
  cp ./graph.obj "s3://${AWS_S3_BUCKET}/graph.otp2.7.0.obj"