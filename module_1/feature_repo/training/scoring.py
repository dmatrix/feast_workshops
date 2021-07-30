from pprint import pprint
from fsutils import get_online_data

if __name__ == "__main__":
    # change this to your location
    FEAST_REPO = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo"
    drivers = [1001]
    for driver in drivers:
        feature_vector = get_online_data(FEAST_REPO, driver)
        print(f"--- Feature Vector for Driver id:{driver} ")
        pprint(feature_vector)
