import csv
import hashlib
import json
import os
import zipfile
from typing import Callable, List, NotRequired, Optional, TypedDict

import requests


class SourceDict(TypedDict):
    url: str
    url_fallback_static: NotRequired[str]
    feed_id: str
    parent_station_name: NotRequired[Callable[[str], str]]
    fix_fares: NotRequired[bool]
    fix_duplicated_routes: NotRequired[bool]


def cyprus_parent_station_name(stop_name: str):
    """
    Generate the parent_station name for Cyprus
    """
    if (stop_name[-1].isdigit() or stop_name[-1].isupper()) and stop_name[-2] == " ":
        return stop_name[:-2]

    return stop_name


sources: List[SourceDict] = [
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C6_google_transit.zip&rel=True",
        "feed_id": "cy-006",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C2_google_transit.zip&rel=True",
        "feed_id": "cy-002",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C4_google_transit.zip&rel=True",
        "feed_id": "cy-004",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C5_google_transit.zip&rel=True",
        "feed_id": "cy-005",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C9_google_transit.zip&rel=True",
        "feed_id": "cy-009",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C10_google_transit.zip&rel=True",
        "feed_id": "cy-010",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://www.motionbuscard.org.cy/opendata/downloadfile?file=GTFS%5C11_google_transit.zip&rel=True",
        "feed_id": "cy-011",
        "parent_station_name": cyprus_parent_station_name,
        "fix_fares": True,
        "fix_duplicated_routes": True
    },
    {
        "url": "https://transport.data.gouv.fr/resources/79642/download",
        "url_fallback_static": "https://cdn1.arno.cl/2024/10/RLA-20241003.zip",
        "feed_id": "fr-rla",
    },
    {
        "url": "https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/",
        "feed_id": "fr-tou",
    },
    {
        "url": "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip",
        "feed_id": "fr-idf",
    },
    {
        "url": "https://github.com/ridewithwagon/kapnos-airport-shuttle-GTFS/raw/refs/heads/main/output.zip",
        "feed_id": "cy-kas",
    }
]


otp_build_config = {
    "transitModelTimeZone": "Europe/Paris",
    "transitFeeds": []
}


def download_and_extract(source: SourceDict):
    """
    Download a GTFS zip, extract it in a folder named with feed_id
    """
    feed_id = source["feed_id"]
    url = source["url"]

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error downloading {url}: {e}")
        if "url_fallback_static" in source:
            print("Trying fallback url")
            response = requests.get(source["url_fallback_static"])
            response.raise_for_status()
        else:
            return

    os.makedirs(feed_id, exist_ok=True)
    with open(f"{feed_id}/{feed_id}.zip", "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(f"{feed_id}/{feed_id}.zip", "r") as zip_ref:
        zip_ref.extractall(f"{feed_id}/")


def fix_fares_attributes(feed_id: str):
    """
    Fix the fares.txt file in the GTFS feed by keeping only the most expensive fare per fare_id.
    """
    fares_file = f"{feed_id}/fare_attributes.txt"

    if not os.path.exists(fares_file):
        print(f"File {fares_file} not found.")
        return

    fares = {}

    with open(fares_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            fare_id = row["fare_id"]
            price = float(row["price"])

            if fare_id not in fares or price > fares[fare_id]["price"]:
                fares[fare_id] = row
                # Ensure price is stored as float
                fares[fare_id]["price"] = price

    with open(fares_file, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ["fare_id", "price", "currency_type",
                      "payment_method", "transfers", "agency_id", "transfer_duration"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for fare in fares.values():
            writer.writerow(fare)


def add_IDFM_fares():
    """
    Add fares to IDFM GTFS feed
    """
    feed_id = "fr-idf"
    ticket_agency_id = "IDFM:71"
    magical_shuttle_route_short_name_map = {
        "Selected": "Villages Nature",
        "Orly": "Orly",
        "CDG": "CDG",
    }

    fare_attributes = "\n".join(
        ["fare_id,price,currency_type,payment_method,transfers,agency_id,transfer_duration",
         f"ticket_bus_tram,2.00,EUR,1,,{ticket_agency_id},5400",
         f"ticket_metro_train_rer,2.50,EUR,1,,{ticket_agency_id},7200",
         f"ticket_airport,13.00,EUR,1,,{ticket_agency_id},7200",
         f"ticket_free,0.00,EUR,0,0,{ticket_agency_id},",
         f"ticket_magical_shuttle,24.00,EUR,1,0,{ticket_agency_id},",
         ])

    fares_rules = "fare_id,route_id,origin_id,destination_id"

    rer_b_airport_stop_ids = [
        "IDFM:monomodalStopPlace:462398", "IDFM:monomodalStopPlace:473364"]
    m_14_airport_stop_ids = ["IDFM:490908", "IDFM:490917"]

    area_airport_stop_ids = rer_b_airport_stop_ids + m_14_airport_stop_ids

    with open(f"{feed_id}/stops.txt", "r", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        stops = list(reader)
        fieldnames = reader.fieldnames

    for stop in stops:
        stop["zone_id"] = "zone_airport" if stop["stop_id"] in area_airport_stop_ids else "zone_default"

    with open(f"{feed_id}/stops.txt", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stops)

    with open(f"{feed_id}/routes.txt", "r") as f:
        reader = csv.DictReader(f)
        routes = list(reader)
        fieldnames = reader.fieldnames

    for route in routes:
        if route["route_short_name"] == "CDG VAL":
            fares_rules += f"\nticket_free,{route['route_id']},,"
            route["route_color"] = "1857B6"
            route["route_text_color"] = "FFFFFF"
        elif route["route_short_name"] in magical_shuttle_route_short_name_map:
            route["route_short_name"] = magical_shuttle_route_short_name_map[
                route["route_short_name"]]
            route["route_color"] = "EB212D"
            route["route_text_color"] = "FFFFFF"
            fares_rules += f"\nticket_magical_shuttle,{route['route_id']},,"
        elif route["route_short_name"] == "ROISSYBUS" or route["route_short_name"] == "ORLYVAL":
            fares_rules += f"\nticket_airport,{route['route_id']},,"
            if route["route_short_name"] == "ORLYVAL":
                route["route_color"] = "2E4D5C"
                route["route_text_color"] = "FFFFFF"
        elif route["route_type"] == "3" or route["route_short_name"] in ["T1", "T2", "T3a", "T3b", "T4", "T5", "T6", "T7", "T8", "T9", "T10"]:
            fares_rules += f"\nticket_bus_tram,{route['route_id']},,"
        else:
            fares_rules += f"\nticket_metro_train_rer,{route['route_id']},zone_default,zone_default"
            fares_rules += f"\nticket_airport,{route['route_id']},zone_default,zone_default"
            fares_rules += f"\nticket_airport,{route['route_id']},zone_airport,zone_default"
            fares_rules += f"\nticket_airport,{route['route_id']},zone_default,zone_airport"

    with open(f"{feed_id}/routes.txt", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(routes)

    files = [("fare_attributes.txt", fare_attributes),
             ("fare_rules.txt", fares_rules)]
    for filename, content in files:
        with open(f"{feed_id}/" + filename, "w") as f:
            f.write(content)


def replace_column_in_file(input_file: str, column: str, mapper: dict[str, str]):
    """
    Replace a column in a file with a mapper
    """
    print(f"Replacing column {column} in {input_file}")
    temp_file = input_file + '.tmp'  # Crée un nom de fichier temporaire

    # Ouvre le fichier d'entrée en lecture et le fichier temporaire en écriture
    with open(input_file, mode='r', newline='', encoding='utf-8-sig') as infile, \
            open(temp_file, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            if row[column] in mapper:
                row[column] = mapper[row[column]]

            writer.writerow(row)

    os.replace(temp_file, input_file)


def fix_duplicated_routes(feed_id: str):
    """
    Fix duplicated routes by merging them based on their short_name and background_color
    """

    # New route id and route details
    routes = {}
    map_old_route_id_to_new_key = {}

    with open(f"{feed_id}/routes.txt", "r", encoding="utf-8-sig") as f:
        header = f.readline().strip().split(",")
        for line in f:
            route = dict(zip(header, line.strip().split(",")))

            # Check if route already exists
            key = hashlib.sha1(
                (route["route_short_name"] + route["route_color"]).encode()).hexdigest()

            map_old_route_id_to_new_key[route["route_id"]] = key
            route["route_id"] = key

            if key not in routes:
                routes[key] = route

    files_to_fix = ["trips.txt", "calendar.txt", "fare_rules.txt"]

    for file in files_to_fix:
        if os.path.exists(f"{feed_id}/{file}"):
            replace_column_in_file(
                f"{feed_id}/{file}", "route_id", map_old_route_id_to_new_key)

    # Remove duplicated routes in routes.txt
    with open(f"{feed_id}/routes.txt", "w") as f:
        f.write(",".join(header) + "\n")
        for route in routes.values():
            f.write(",".join([route.get(h, "") for h in header]) + "\n")


def stop_name_to_id(stop_name: str):
    """
    Return sha1 of stop_name
    """
    return hashlib.sha1(stop_name.encode()).hexdigest()


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
            parent_station_id = stop_name_to_id(parent_station_name)
            if parent_station_name not in parent_stations:
                parent_stations[parent_station_name] = {
                    "stop_id": parent_station_id,
                    "stop_name": parent_station_name,
                    "stop_lat": stop["stop_lat"],
                    "stop_lon": stop["stop_lon"],
                    "location_type": "1"
                }
            stop["parent_station"] = parent_station_id

    if "parent_station" not in header:
        header.append("parent_station")

    if "location_type" not in header:
        header.append("location_type")

    # Write the new stops.txt file
    with open(f"{feed_id}/stops.txt", "w") as f:
        f.write(",".join(header) + "\n")
        for parent_station in parent_stations.values():
            f.write(
                ",".join([parent_station.get(h, "") for h in header]) + "\n")
        for stop in stops:
            f.write(",".join([stop.get(h, "") for h in header]) + "\n")


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

    if only is not None:
        otp_build_config["osm"] = []

    with open("build-config.json", "w") as f:
        f.write(json.dumps(otp_build_config, indent=2))


def generate_otp_config():
    """
    Generate the otp-config.json for OTP
    """
    otp_config = {
        "otpFeatures": {
            "FaresV2": True
        }
    }

    with open("otp-config.json", "w") as f:
        f.write(json.dumps(otp_config, indent=2))


def main(only: Optional[str] = None, zip: bool = False):
    generate_otp_build_config(only)
    generate_otp_config()

    for source in sources:
        if only is not None and source["feed_id"] != only:
            continue

        download_and_extract(source)
        feed_id = source["feed_id"]

        if "fix_fares" in source and source["fix_fares"]:
            fix_fares_attributes(feed_id)

        if "parent_station_name" in source and source["parent_station_name"]:
            auto_generate_parent_stations(
                feed_id, source["parent_station_name"])

        if "fix_duplicated_routes" in source and source["fix_duplicated_routes"]:
            fix_duplicated_routes(feed_id)

        if feed_id == "fr-idf":
            add_IDFM_fares()

    if only and zip:
        with zipfile.ZipFile(f"{only}.zip", "w") as zipf:
            for root, dirs, files in os.walk(only):
                for file in files:
                    if file.endswith(".txt"):
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file), only))


if __name__ == "__main__":
    main()
