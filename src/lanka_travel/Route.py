import os

from utils import JSONFile, Log

from utils_future import LatLng

log = Log("Route")


class Route:
    DIR_DATA = os.path.join("data", "routes")

    @staticmethod
    def clean_place_name(place_name: str) -> str:
        return place_name.replace(" ", "")

    def __init__(
        self,
        start_place_name: str,
        end_place_name: str,
        latlng_list: list[LatLng],
    ):
        self.start_place_name = Route.clean_place_name(start_place_name)
        self.end_place_name = Route.clean_place_name(end_place_name)
        self.latlng_list = latlng_list

    def __len__(self):
        return len(self.latlng_list)

    @property
    def file_name(self) -> str:
        return f"{self.start_place_name}-{self.end_place_name}.json"

    @property
    def file_path(self) -> str:
        return os.path.join(Route.DIR_DATA, self.file_name)

    def to_file(self):
        JSONFile(self.file_path).write(
            [latlng.to_list() for latlng in self.latlng_list]
        )
        log.info(f"Wrote {len(self)} points to {self.file_path}")

    @staticmethod
    def from_file(file_path: str) -> "Route":
        base_name = os.path.basename(file_path)
        start_place_name, end_place_name = base_name.split(".")[0].split("-")
        latlng_list = LatLng.list_from_file(file_path)
        return Route(start_place_name, end_place_name, latlng_list)

    @staticmethod
    def list_all() -> list["Route"]:
        route_list = []
        for root, ___, files in os.walk(Route.DIR_DATA):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    route = Route.from_file(file_path)
                    route_list.append(route)

        log.info(f"Loaded {len(route_list):,} routes from {Route.DIR_DATA}")
        return route_list
