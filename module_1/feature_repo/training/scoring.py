from pprint import pprint
from fsutils import get_online_data

if __name__ == "__main__":
    FEAST_REPO = "/Users/jules/git-repos/feature_repo"
    drivers = [1001, 1002, 1003]
    for driver in drivers :
        feature_vector = get_online_data(FEAST_REPO, driver)
        print(f"--- Feature Vector for Driver id:{driver} ")
        pprint(feature_vector)
