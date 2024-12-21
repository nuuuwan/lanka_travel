from gig import Ent, EntType

from lanka_travel.Place import Place


class LankaTravel:
    def __init__(self, place_list: list[Place]):
        self.place_list = place_list

    def get_region_ent_list(self, region_ent_type: EntType) -> list[Ent]:
        return []
