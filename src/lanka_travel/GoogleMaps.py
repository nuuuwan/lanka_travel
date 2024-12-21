import os
from functools import cache

import googlemaps
from utils import JSONFile, Log

log = Log("GoogleMaps")


class GoogleMaps:
    def __init__(self, mode="driving"):
        self.mode = mode

    @staticmethod
    @cache
    def decode_polyline(polyline_str):
        index, lat, lng = 0, 0, 0
        latlng_list = []
        changes = {"latitude": 0, "longitude": 0}

        while index < len(polyline_str):
            for unit in ["latitude", "longitude"]:
                shift, result = 0, 0

                while True:
                    byte = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (byte & 0x1F) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break

                if result & 1:
                    changes[unit] = ~(result >> 1)
                else:
                    changes[unit] = result >> 1

            lat += changes["latitude"]
            lng += changes["longitude"]

            latlng_list.append([lat / 100000.0, lng / 100000.0])

        return latlng_list

    @property
    def gmaps(self):
        api_key = os.environ["GMAPS_API_KEY"]
        gmaps = googlemaps.Client(key=api_key)
        return gmaps

    @cache
    def get_latlng(self, search_text):
        results = self.gmaps.geocode(search_text)
        if not results:
            return None
        geocode_result = results[0]
        location = geocode_result["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
        log.debug(f"{search_text} -> ({lat}, {lng})")
        return [lat, lng]

    @cache
    def get_latlng_list_for_route(self, start_search_text, end_search_text):
        results = self.gmaps.directions(
            start_search_text,
            end_search_text,
            mode=self.mode,
        )

        if len(results) == 0:
            log.error("No results...")
            return []
        result = results[0]
        latlng_list = self.decode_polyline(
            result["overview_polyline"]["points"]
        )
        log.info(
            f"Found {len(latlng_list)} points for"
            + f" {start_search_text} -> {end_search_text}"
        )
        return latlng_list

    def save_path(self, id, start_search_text, end_search_text):

        file_path = os.path.join("data", "routes", "road", f"{id}.json")
        if os.path.exists(file_path):
            log.debug(f"Exists {file_path}")
            return
        JSONFile(file_path).write(
            self.get_latlng_list_for_route(
                start_search_text,
                end_search_text,
            )
        )
        log.info(f"Wrote {file_path}")


if __name__ == "__main__":

    for start_search_text, end_search_text in [
        ("Colombo", "Galle"),
        ("Colombo", "Kandy"),
        ("Ambepussa", "Dambulla"),
        ("Dambulla", "Anuradhapura"),
        ("Dambulla", "Habarana"),
        ("Habarana", "Trincomalee"),
        ("Habarana", "Polonnaruwa"),
        ("Polonnaruwa", "Passikuda"),
        ("Ratnapura", "Haputale"),
        ("Haputale", "Ella"),
        ("Ella", "Kataragama"),
        ("Colombo", "Kataragama"),
        ("Colombo", "Maravila"),
        ("Colombo", "Avissawella"),
        ("Avissawella", "Ratnapura"),
        ("Avissawella", "Nuwara Eliya"),
        ("Kandy", "Pussellawa"),
        ("Pussellawa", "Nuwara Eliya"),
        ("Colombo", "Panadura"),
        ("Panadura", "Bentota"),
        ("Bentota", "Galle"),
        ("Galle", "Matara"),
        ("Matara", "Kamburupitiya"),
        ("Colombo", "Kurunegala"),
        ("Kurunegala", "Kandy"),
        ("Kandy", "Matale"),
        ("Nuwara Eliya", "Badulla"),
        ("Nuwara Eliya", "Horton Plains"),
        ("Horton Plains", "Ohiya"),
        ("Ohiya", "Haputale"),
        ("Hambantota", "Yala"),
        ("Ratnapura", "Uda Walawe"),
        ("Kandy", "Randenigala"),
        ("Randenigala", "Mahiyangana"),
    ]:
        id = f"{start_search_text}-{end_search_text}".replace(" ", "")
        GoogleMaps("driving").save_path(
            id,
            f"{start_search_text}, Sri Lanka",
            f"{end_search_text}, Sri Lanka",
        )
