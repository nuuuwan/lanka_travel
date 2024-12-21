from gig import EntType

from lanka_travel import LankaTravel, Place

if __name__ == "__main__":
    latlng_list = [
        (6.9271, 79.8612),
    ]
    place_list = [Place(latlng) for latlng in latlng_list]
    lanka_travel = LankaTravel(place_list)
    lanka_travel.get_region_ent_list(EntType.PROVINCE)
