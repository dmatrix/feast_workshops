from pathlib import Path
from pprint import pprint
from feast import FeatureStore


def get_feature_vector(rpath: Path, id) -> dict:
    store = FeatureStore(repo_path=rpath)

    # get the feature service associated with this store
    feature_service = store.get_feature_service("driver_ranking_fv_svc")

    # Retrieve training data from local parquet FileSource
    feature_vector = store.get_online_features(
        entity_rows=[{"driver_id": id}],
        features=feature_service
    ).to_df()

    return feature_vector


if __name__ == '__main__':
    f_vector = get_feature_vector(Path("../"), 1001)
    pprint(f_vector)