python3 prepare_gtfs.py

java -Xmx4G -jar otp-2.5.0-shaded.jar --build --save .

mkdir external
mv ./graph.obj ./external/graph.obj

# python3 upload.py