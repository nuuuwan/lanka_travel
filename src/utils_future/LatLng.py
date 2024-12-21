from shapely import Point


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

    def to_point(self):
        return Point(self.lng, self.lat)
