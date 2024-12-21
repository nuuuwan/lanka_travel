import os
from functools import cache

import googlemaps
from utils import Log

from lanka_travel.Route import Route
from utils_future import LatLng

log = Log("GoogleMaps")


class GoogleMaps:
    def __init__(self, mode="driving"):
        self.mode = mode
        self.gmaps = googlemaps.Client(key=os.environ["GMAPS_API_KEY"])

    @staticmethod
    @cache
    def __decode_polyline__(polyline_str: str) -> list[LatLng]:
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
            latlng = LatLng(lat / 100000.0, lng / 100000.0)
            latlng_list.append(latlng)

        return latlng_list

    def get_route(self, start_place_name: str, end_place_name: str):
        PREFIX = ", Sri Lanka"
        results = self.gmaps.directions(
            start_place_name + PREFIX,
            end_place_name + PREFIX,
            mode=self.mode,
        )

        if len(results) == 0:
            log.error("No results...")
            return None

        result = results[0]
        latlng_list = self.__decode_polyline__(
            result["overview_polyline"]["points"]
        )

        return Route(start_place_name, end_place_name, latlng_list)
