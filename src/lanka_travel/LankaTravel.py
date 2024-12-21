import os

import matplotlib.pyplot as plt
from gig import Ent, EntType
from utils import Hash, JSONFile, Log

from lanka_travel.Geo import Geo

log = Log("LankaTravel")


class LankaTravel:
    DIR_DATA_ROUTES = os.path.join("data", "routes")
    DIR_DATA_IDX = os.path.join("data", "idx")
    COLOR_IDX = {
        EntType.PROVINCE.name: "#f001",
        EntType.DISTRICT.name: "#f003",
        EntType.DSD.name: "#f008",
        EntType.GND.name: "#f00f",
    }

    EDGE_COLOR_IDX = {
        EntType.PROVINCE.name: "#888f",
        EntType.DISTRICT.name: "#8888",
        EntType.DSD.name: "#8880",
        EntType.GND.name: "#8880",
    }

    def __init__(self, latlng_list_list: list[list[tuple]]):
        self.latlng_list_list = latlng_list_list

    @staticmethod
    def get_region_idx_for_latlng_list(latlng_list) -> dict[str, list[str]]:
        h = Hash.md5(str(latlng_list))[:4]
        idx_file_path = os.path.join(LankaTravel.DIR_DATA_IDX, f"{h}.json")
        if os.path.exists(idx_file_path):
            idx = JSONFile(idx_file_path).read()
            log.debug(f"Read {idx_file_path}")
            return idx

        idx = LankaTravel.get_region_idx_for_latlng_list_nocache(latlng_list)
        JSONFile(idx_file_path).write(idx)
        log.info(f"Wrote {idx_file_path}")
        return idx

    @staticmethod
    def get_region_idx_for_latlng_list_nocache(
        latlng_list,
    ) -> dict[str, list[str]]:

        idx = {}
        n = len(latlng_list)
        for i, latlng in enumerate(latlng_list, start=1):
            idx_item = Geo.get_latlng_regions(latlng)
            print(f"{i}/{n} {latlng} -> {idx_item}", end="\r")

            for ent_type_name, id in idx_item.items():
                if ent_type_name not in idx:
                    idx[ent_type_name] = set()
                idx[ent_type_name].add(id)
        idx = {k: list(sorted(v)) for k, v in idx.items()}

        return idx

    def get_region_idx(self) -> dict[str, list[str]]:
        idx = {}
        for latlng_list in self.latlng_list_list:
            idx_item = self.get_region_idx_for_latlng_list(latlng_list)
            for ent_type_name, region_ids in idx_item.items():
                if ent_type_name not in idx:
                    idx[ent_type_name] = set()
                idx[ent_type_name].update(region_ids)
        idx = {k: list(sorted(v)) for k, v in idx.items()}
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

    @staticmethod
    def all():
        #  in os.walk("data"):
        latlng_list_list = []
        for root, ___, files in os.walk(LankaTravel.DIR_DATA_ROUTES):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    latlng_list = JSONFile(file_path).read()
                    log.debug(
                        f"Read {len(latlng_list):,} latlngs from {file_path}"
                    )
                    latlng_list_list.append(latlng_list)
        log.info(
            f"Loaded {len(latlng_list_list):,}"
            + f" latlng_lists from {LankaTravel.DIR_DATA_ROUTES}"
        )
        return LankaTravel(latlng_list_list)
