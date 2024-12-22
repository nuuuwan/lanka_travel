import os
from functools import cache

import geopandas
from gig import EntType
from shapely.geometry import mapping, shape
from utils import JSONFile, Log

from utils_future import LatLng

log = Log("Geo")


class Geo:

    IDX_PATH = os.path.join("data", "latlng_to_region_id.json")
    IDX_JSON_FILE = JSONFile(IDX_PATH)

    ENT_TYPE_LIST = [
        EntType.PROVINCE,
        EntType.DISTRICT,
        EntType.DSD,
        EntType.GND,
    ]

    @staticmethod
    def load_idx():
        if Geo.IDX_JSON_FILE.exists:
            return Geo.IDX_JSON_FILE.read()
        return {}

    def __init__(self):
        self.idx = Geo.load_idx()
        for ent_type in self.ENT_TYPE_LIST:
            self.__get_all_geodata__(ent_type.name)

    def store_idx(self):
        sorted_idx = dict(sorted(self.idx.items(), key=lambda item: item[0]))
        Geo.IDX_JSON_FILE.write(sorted_idx)
        n = len(sorted_idx)
        log.info(f"Stored {n} mappings to {Geo.IDX_PATH}")

    @cache
    def __get_all_geodata__(self, region_ent_type_name):
        FILE_EXT = "topojson"
        url = (
            "https://raw.githubusercontent.com"
            + "/nuuuwan/geo-data/refs/heads/main"
            + f"/{region_ent_type_name}.{FILE_EXT}"
        )
        data = geopandas.read_file(url)
        log.debug(f"Read {url}")
        return data

    def __get_region_to_geo__(self, region_ent_type: EntType) -> dict:
        geo_data = self.__get_all_geodata__(region_ent_type.name)
        n_regions = len(geo_data["geometry"])
        region_to_geo = {}
        for i in range(0, n_regions):
            region_id = geo_data["id"][i]
            region_to_geo[region_id] = mapping(geo_data["geometry"][i])
        return region_to_geo

    def __get_latlng_region__(
        self,
        latlng: LatLng,
        region_ent_type: EntType,
        parent_region_id: str = None,
    ) -> str:
        point = latlng.to_point()
        region_to_geo = self.__get_region_to_geo__(region_ent_type)
        for region_id, geo in region_to_geo.items():
            if parent_region_id and (parent_region_id not in region_id):
                continue
            multi_polygon = shape(geo)
            for polygon in multi_polygon.geoms:
                if polygon.contains(point):
                    return region_id
        return None

    def __get_region_id_nocache__(self, latlng: LatLng) -> str:

        region_id = None
        parent_region_id = None
        for region_ent_type in self.ENT_TYPE_LIST:
            region_id = self.__get_latlng_region__(
                latlng, region_ent_type, parent_region_id
            )
            if not region_id:
                break
            parent_region_id = region_id

        return region_id

    def get_region_id(self, latlng: LatLng) -> str:
        if str(latlng) in self.idx:
            return self.idx[str(latlng)]

        region_id = self.__get_region_id_nocache__(latlng)
        self.idx[str(latlng)] = region_id

        return region_id
