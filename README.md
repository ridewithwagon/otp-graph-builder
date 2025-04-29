# OTP Graph Builder

This repo contains a Docker container in charge of building a graph for OTP (Open Trip Planner). This graph is consummed by Wagon.

Some GTFS files are enhanced with additionnal data (Fares, Shapes) and are uploaded separately to a bucket. 

Included in street graph : 
- Ile de France
- Toulouse
- Nice
- Chypre (UE)

Included GTFS :
- Ile de France Mobilités (IDFM)
- Toulouse (Tisséo)
- Nice (Lignes d'Azur) — __Unstable__
- Chypre (EMEL (Limassol), OSYPA (Pafos), OSEA (Famagusta), NPT (Nicosia) LPT (Larnaca), Intercity, Pame Express (Park and Ride))
- Chypre - Kapnos Airport Shuttle - __Unstable__

# Available files 

All files are updated everyday during the night. 

- [`graph.otp2.7.0.obj`](https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/graph.otp2.7.0.obj) OTP graph file
- [`streetGraph.otp2.7.0.obj`](https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/streetGraph.otp2.7.0.obj) OTP street graph file (updated each month)
- [`fr-idf.zip`](https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/fr-idf.zip) IDFM GTFS with added features : Fares, Shapes, Routes names fix.
    > [!IMPORTANT]  
    > Fares are created manually and can be outdated at any moment.
- [`cy-kas.zip`](https://r2-wnam-wagon-prodassets-otp-graph.arno.cl/cy-kas.zip) Kapnos Airport Shuttle GTFS with added features : Shapes.

You are free to use theses files in your apps. Please credit Open Street Map Contributors.