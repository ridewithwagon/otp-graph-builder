import json

otp_build_config = {
    "osm": [
        {
            "source": "https://download.geofabrik.de/europe/cyprus-latest.osm.pbf"
        },
        {
            "source": "https://cdn1.arno.cl/2024/09/toulouse.osm.pbf"
        },
        {
            "source": "https://cdn1.arno.cl/2024/05/nice.osm.pbf"
        }
    ],
}

if __name__ == "__main__":
    with open("build-config.json", "w") as f:
        json.dump(otp_build_config, f)
