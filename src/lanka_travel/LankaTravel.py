import os
from functools import cached_property

import matplotlib.pyplot as plt
from gig import Ent, EntType
from utils import Log, Parallel

from lanka_travel.Geo import Geo
from lanka_travel.Route import Route
from utils_future import LatLng

log = Log("LankaTravel")


class LankaTravel:
    BASE_COLOR = "#ff0000"
    COLOR_IDX = {
        EntType.PROVINCE.name: BASE_COLOR + "08",
        EntType.DISTRICT.name: BASE_COLOR + "10",
        EntType.DSD.name: BASE_COLOR + "20",
        EntType.GND.name: BASE_COLOR + "ff",
    }

    EDGE_COLOR_IDX = {
        EntType.PROVINCE.name: "#888f",
        EntType.DISTRICT.name: "#8888",
        EntType.DSD.name: "#8880",
        EntType.GND.name: "#8880",
    }

    def __init__(self, route_list: list[Route]):
        self.route_list = route_list

    @cached_property
    def latlng_list(self) -> list[LatLng]:
        latlng_list = []
        for route in self.route_list:
            latlng_list.extend(route.latlng_list)
        return list(set(latlng_list))

    @staticmethod
    def __get_region_idx_part__(geo, latlng):
        region_id = geo.get_region_id(latlng)

        return {
            "province": region_id[:4],
            "district": region_id[:5],
            "dsd": region_id[:7],
            "gnd": region_id[:10],
        }

    def get_region_idx(self) -> dict[str, list[str]]:

        geo = Geo()
        n = len(self.latlng_list)
        workers = []
        for i, latlng in enumerate(self.latlng_list):

            def worker(i=i, latlng=latlng):
                idx_part = self.__get_region_idx_part__(geo, latlng)
                print(f"{i}/{n} {latlng} -> {idx_part['gnd']}", end="\r")
                return idx_part

            workers.append(worker)

        idx_party_list = Parallel.run(workers, max_threads=16)
        idx = {}
        for idx_part in idx_party_list:
            for region_ent_type_name, region_id in idx_part.items():
                if region_ent_type_name not in idx:
                    idx[region_ent_type_name] = set()
                idx[region_ent_type_name].add(region_id)
        geo.store_idx()
        return idx

    def draw(self):
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        title_items = []

        for (
            region_ent_type_name,
            region_id_list,
        ) in self.get_region_idx().items():
            title_item = self.__plot_regions__(
                ax, region_ent_type_name, region_id_list
            )
            title_items.append(title_item)

        self.__plot_finalize__(title_items)

    def __plot_regions__(self, ax, region_ent_type_name, region_id_list):
        color = self.COLOR_IDX.get(region_ent_type_name, "#ccc")
        edgecolor = self.EDGE_COLOR_IDX.get(region_ent_type_name, "#888")
        n = len(region_id_list)
        title_item = f"{n:,} {region_ent_type_name}s"
        log.debug(f"Plotting {title_item}")

        for i, region_id in enumerate(region_id_list, start=1):
            ent = Ent.from_id(region_id)
            geo = None
            try:
                geo = ent.geo()
            except Exception as e:
                log.error(f"Error plotting {ent.id}: {e}")
                continue
            geo.plot(ax=ax, color=color, edgecolor=edgecolor)
            print(f"{i}/{n} {ent.id}", end="\r")

        return title_item

    def __plot_finalize__(self, title_items):
        title = " | ".join(title_items)
        plt.title(title)

        image_path = "lanka_travel.png"
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f"Saved {image_path}")
        os.startfile(image_path)
