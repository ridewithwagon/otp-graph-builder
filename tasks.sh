python3 prepare_gtfs.py

java -Xmx4G -jar otp-2.5.0-shaded.jar --build --save .

python3 upload.py