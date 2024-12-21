import os

from utils import JSONFile, Log

from utils_future import LatLng

log = Log("Route")


class Route:
    DIR_DATA = os.path.join("data", "routes")

    def __init__(self, latlng_list: list[LatLng]):
        self.latlng_list = latlng_list

    @staticmethod
    def from_file(file_path: str):
        return Route(JSONFile(file_path).read())

    @staticmethod
    def list_all():
        route_list = []
        for root, ___, files in os.walk(Route.DIR_DATA):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    route = Route.from_file(file_path)
                    route_list.append(route)
        log.info(f"Loaded {len(route_list):,} routes from {Route.DIR_DATA}")
        return route_list
