from functools import cache

import geopandas
from gig import EntType
from shapely.geometry import Point, mapping, shape
from utils import Log

log = Log("Geo")


class Geo:

    @staticmethod
    @cache
    def get_all_geodata(region_ent_type_name):

        file_ext = "topojson"
        url = (
            "https://raw.githubusercontent.com"
            + "/nuuuwan/geo-data/refs/heads/main"
            + f"/{region_ent_type_name}.{file_ext}"
        )
        data = geopandas.read_file(url)
        log.debug(f"Read {url}")
        return data

    @staticmethod
    @cache
    def _get_region_to_geo(region_ent_type_name):
        """Get region to geo index."""
        geo_data = Geo.get_all_geodata(region_ent_type_name)
        n_regions = len(geo_data["geometry"])
        region_to_geo = {}
        for i in range(0, n_regions):
            region_id = geo_data["id"][i]
            region_to_geo[region_id] = mapping(geo_data["geometry"][i])
        return region_to_geo

    @staticmethod
    def _get_latlng_region(lat_lng, region_ent_type, parent_region_id=None):

        lat, lng = lat_lng
        point = Point(lng, lat)

        region_to_geo = Geo._get_region_to_geo(region_ent_type.name)

        for region_id, geo in region_to_geo.items():
            if parent_region_id and (parent_region_id not in region_id):
                continue
            multi_polygon = shape(geo)
            for polygon in multi_polygon.geoms:
                if polygon.contains(point):
                    return region_id

        return None

    @staticmethod
    def get_latlng_regions(lat_lng):

        idx = {}
        parent_region_id = ""
        for region_ent_type in [
            EntType.PROVINCE,
            EntType.DISTRICT,
            EntType.DSD,
            EntType.GND,
        ]:
            region_id = Geo._get_latlng_region(
                lat_lng, region_ent_type, parent_region_id
            )
            if not region_id:
                break
            idx[region_ent_type.name] = region_id
            parent_region_id = region_id

        return idx
