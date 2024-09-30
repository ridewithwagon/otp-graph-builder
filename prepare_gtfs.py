import requests
import os
import zipfile
import json
from typing import Callable, TypedDict, List, Optional


class SourceDict(TypedDict):
    url: str
    feed_id: str
    parent_station_name: Optional[Callable[[str], str]]
    fix_fares: bool


def cyprus_parent_station_name(stop_name: str):
    """
    Generate the parent_station name for Cyprus
    """
    return stop_name.split(" - ")[0]


sources: List[SourceDict] = [
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C6_google_transit.zip&rel=True",
        "feed_id": "cy-006",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C2_google_transit.zip&rel=True",
        "feed_id": "cy-002",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": False
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C4_google_transit.zip&rel=True",
        "feed_id": "cy-004",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C5_google_transit.zip&rel=True",
        "feed_id": "cy-005",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": False
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C9_google_transit.zip&rel=True",
        "feed_id": "cy-009",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": False
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C10_google_transit.zip&rel=True",
        "feed_id": "cy-010",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": False
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C11_google_transit.zip&rel=True",
        "feed_id": "cy-011",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": False
    },
    {
        # "url": "https://transport.data.gouv.fr/resources/79642/download",
        "url": "https://opendata.nicecotedazur.org/data/dataset/export-quotidien-au-format-gtfs-du-reseau-de-transport-lignes-d-azur/resource/aacb4eea-d008-4b13-b17a-848b8ced7e03/download",
        "feed_id": "fr-rla",
        "parent_station_name": None,
        "fix_fares": False
    },
    {
        "url": "https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/",
        "feed_id": "fr-tou",
        "parent_station_name": None,
        "fix_fares": False
    }
]


otp_build_config = {
    "transitModelTimeZone": "Europe/Paris",
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
    "transitFeeds": []
}


def download_and_extract(source: SourceDict):
    """
    Download a GTFS zip, extract it in a folder named with feed_id
    """
    feed_id = source["feed_id"]
    url = source["url"]
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(feed_id, exist_ok=True)
    with open(f"{feed_id}/{feed_id}.zip", "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(f"{feed_id}/{feed_id}.zip", "r") as zip_ref:
        zip_ref.extractall(f"{feed_id}/")


def fix_fares_attributes(feed_id: str):
    """
    Fix the fares.txt file in the GTFS feed
    """
    # TODO: Parse file to detect fares_rules errors
    os.remove(f"{feed_id}/fare_rules.txt")
    os.remove(f"{feed_id}/fare_attributes.txt")


def auto_generate_parent_stations(feed_id: str, get_parent_station_name: Callable[[str], str]):
    """
    Find all stops without parent_station and generate the parent_station
    """

    # Save all stops in a list of dicts
    stops = []
    with open(f"{feed_id}/stops.txt", "r", encoding="utf-8-sig") as f:
        header = f.readline().strip().split(",")
        for line in f:
            stop = dict(zip(header, line.strip().split(",")))
            stops.append(stop)

    parent_stations = {}

    # Find all stops without parent_station
    for stop in stops:
        if "parent_station" not in stop or stop["parent_station"] == "":
            parent_station_name = get_parent_station_name(stop["stop_name"])
            parent_station_id = f"{parent_station_name}::auto_generated"
            if parent_station_name not in parent_stations:
                parent_stations[parent_station_name] = {
                    "stop_id": parent_station_id,
                    "stop_name": parent_station_name,
                    "stop_lat": stop["stop_lat"],
                    "stop_lon": stop["stop_lon"],
                    "location_type": 1
                }
            stop["parent_station"] = parent_station_id

    if "parent_station" not in header:
        header.append("parent_station")

    # Write the new stops.txt file
    with open(f"{feed_id}/stops.txt", "w") as f:
        f.write(",".join(header) + "\n")
        for stop in stops:
            f.write(",".join([stop.get(h, "") for h in header]) + "\n")
        for parent_station in parent_stations.values():
            f.write(
                ",".join([parent_station.get(h, "") for h in header]) + "\n")


def cat(file: str, line_contains: Optional[str] = None):
    with open(file, "r") as f:
        for line in f:
            if line_contains is None or line_contains in line:
                print(line.strip())


def generate_otp_build_config(only: Optional[str] = None):
    """
    Generate the build-config.json for OTP
    """
    for source in sources:
        if only is not None and source["feed_id"] != only:
            continue

        otp_build_config["transitFeeds"].append({
            "source": f"./{source['feed_id']}/",
            "type": "gtfs",
            "feedId": source["feed_id"]
        })

    with open("build-config.json", "w") as f:
        f.write(json.dumps(otp_build_config, indent=2))


def main(only: Optional[str] = None):
    generate_otp_build_config(only)

    for source in sources:
        if only is not None and source["feed_id"] != only:
            continue

        download_and_extract(source)
        feed_id = source["feed_id"]

        if source["fix_fares"]:
            fix_fares_attributes(feed_id)

        if source["parent_station_name"]:
            auto_generate_parent_stations(
                feed_id, source["parent_station_name"])


if __name__ == "__main__":
    main(only="cy-009")
