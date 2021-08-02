from pathlib import Path
from pprint import pprint
from feast import FeatureStore


def get_feature_vector(rpath: Path, id) -> dict:
    store = FeatureStore(repo_path=rpath)

    feature_vector=store.get_online_features(
            feature_refs=[
                "driver_hourly_stats:conv_rate",
                "driver_hourly_stats:acc_rate",
                "driver_hourly_stats:avg_daily_trips",
            ],
            entity_rows=[{"driver_id": id}],
        ).to_dict()

    return feature_vector


if __name__ == '__main__':
    f_vector = get_feature_vector(Path("../"), 1002)
    pprint(f_vector)