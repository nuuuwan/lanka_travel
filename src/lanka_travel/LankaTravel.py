import os

import matplotlib.pyplot as plt
from gig import Ent, EntType
from utils import JSONFile, Log

from lanka_travel.Geo import Geo

log = Log("LankaTravel")


class LankaTravel:
    DIR_DATA = "data"
    COLOR_IDX = {
        EntType.PROVINCE.name: "#f001",
        EntType.DISTRICT.name: "#f002",
        EntType.DSD.name: "#f004",
        EntType.GND.name: "#f00f",
    }

    EDGE_COLOR_IDX = {
        EntType.PROVINCE.name: "#888f",
        EntType.DISTRICT.name: "#8888",
        EntType.DSD.name: "#8880",
        EntType.GND.name: "#8880",
    }

    def __init__(self, latlng_list: list[tuple]):
        self.latlng_list = latlng_list

    def get_region_idx(self) -> dict[str, list[str]]:
        idx = {}
        n = len(self.latlng_list)
        for i, latlng in enumerate(self.latlng_list, start=1):
            idx_item = Geo.get_latlng_regions(latlng)
            log.debug(f"{i}/{n} {latlng} -> {idx_item}")

            for ent_type_name, id in idx_item.items():
                if ent_type_name not in idx:
                    idx[ent_type_name] = set()
                idx[ent_type_name].add(id)
        return {k: list(sorted(v)) for k, v in idx.items()}

    def draw(self):
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        for (
            region_ent_type_name,
            region_id_list,
        ) in self.get_region_idx().items():
            color = self.COLOR_IDX.get(region_ent_type_name, "#ccc")
            edgecolor = self.EDGE_COLOR_IDX.get(region_ent_type_name, "#888")
            for region_id in region_id_list:
                ent = Ent.from_id(region_id)
                try:
                    ent.geo().plot(ax=ax, color=color, edgecolor=edgecolor)
                    log.debug(f"Plotted {ent.id}")
                except Exception as e:
                    log.error(f"Error plotting {ent.id}: {e}")
        image_path = "lanka_travel.png"
        plt.savefig(image_path, dpi=100)
        plt.close()
        log.info(f"Saved {image_path}")
        os.startfile(image_path)

    @staticmethod
    def all():
        #  in os.walk("data"):
        all_latlng_list = []
        for root, ___, files in os.walk(LankaTravel.DIR_DATA):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    latlng_list = JSONFile(file_path).read()
                    log.debug(
                        f"Read {len(latlng_list):,} latlngs from {file_path}"
                    )
                    all_latlng_list.extend(latlng_list)
        log.info(
            f"Loaded {len(all_latlng_list):,}"
            + f" latlngs from {LankaTravel.DIR_DATA}"
        )
        return LankaTravel(all_latlng_list)
