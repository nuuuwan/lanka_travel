if __name__ == "__main__":
    from lanka_travel import GoogleMaps

    for start_place_name, end_place_name in [
        ("Colombo", "Galle"),
        ("Colombo", "Kandy"),
        ("Ambepussa", "Dambulla"),
        ("Dambulla", "Anuradhapura"),
        ("Dambulla", "Habarana"),
        ("Habarana", "Trincomalee"),
        ("Habarana", "Polonnaruwa"),
        ("Polonnaruwa", "Passikuda"),
        ("Ratnapura", "Haputale"),
        ("Haputale", "Ella"),
        ("Ella", "Kataragama"),
        ("Colombo", "Kataragama"),
        ("Colombo", "Maravila"),
        ("Colombo", "Avissawella"),
        ("Avissawella", "Ratnapura"),
        ("Avissawella", "Nuwara Eliya"),
        ("Kandy", "Pussellawa"),
        ("Pussellawa", "Nuwara Eliya"),
        ("Colombo", "Panadura"),
        ("Panadura", "Bentota"),
        ("Bentota", "Galle"),
        ("Galle", "Matara"),
        ("Matara", "Kamburupitiya"),
        ("Colombo", "Kurunegala"),
        ("Kurunegala", "Kandy"),
        ("Kandy", "Matale"),
        ("Nuwara Eliya", "Badulla"),
        ("Nuwara Eliya", "Horton Plains"),
        ("Horton Plains", "Ohiya"),
        ("Ohiya", "Haputale"),
        ("Hambantota", "Yala"),
        ("Ratnapura", "Uda Walawe"),
        ("Kandy", "Randenigala"),
        ("Randenigala", "Mahiyangana"),
    ]:
        route = GoogleMaps("driving").get_route(
            start_place_name,
            end_place_name,
        )
        route.to_file()
