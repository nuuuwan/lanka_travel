from shapely import Point
from utils import JSONFile


class LatLng:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return f"{self.lat:.6f},{self.lng:.6f}"

    def __eq__(self, other):
        return self.lat == other.lat and self.lng == other.lng

    def __hash__(self):
        return hash(str(self))

    def to_list(self):
        return [self.lat, self.lng]

    def to_point(self):
        return Point(self.lng, self.lat)

    @staticmethod
    def list_from_file(file_path: str) -> list["LatLng"]:
        return [LatLng(lat, lng) for lat, lng in JSONFile(file_path).read()]
