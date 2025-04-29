import csv


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
        elif route["route_short_name"] in ["N1", "N2"]:
            fares_rules += f"\nticket_free,{route['route_id']},,"
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
            fares_rules += f"\nticket_airport,{route['route_id']},zone_airport,zone_airport"

    with open(f"{feed_id}/routes.txt", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(routes)

    files = [("fare_attributes.txt", fare_attributes),
             ("fare_rules.txt", fares_rules)]
    for filename, content in files:
        with open(f"{feed_id}/" + filename, "w") as f:
            f.write(content)
