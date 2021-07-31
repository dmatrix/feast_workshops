from pprint import pprint
from feast import FeatureStore


if __name__ == "__main__":
    # change this to your location
    FEAST_REPO = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo"
    store = FeatureStore(repo_path=FEAST_REPO)

    feature_vector = store.get_online_features(
        feature_refs=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
        ],
        entity_rows=[{"driver_id": 1001}],
    ).to_dict()

    pprint(feature_vector)
