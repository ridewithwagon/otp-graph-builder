# On ne génère les rues que le premier du mois
if [ $(date +%d) -eq 1 ]; then
    python3 prepare_osm.py
    java -Xmx20G -jar otp-2.6.0-shaded.jar --buildStreet .
else
    wget https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/streetGraph.obj
fi

python3 prepare_gtfs.py

java -Xmx20G -jar otp-2.6.0-shaded.jar --loadStreet --save .

mkdir external
cp ./graph.obj ./external/graph.obj

python3 upload.py