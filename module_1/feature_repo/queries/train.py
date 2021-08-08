import pandas as pd
from pathlib import Path
from datetime import datetime
from feast import FeatureStore


def get_training_data(rpath:Path) -> dict:
    entity_df = pd.DataFrame.from_dict(
        {
            "driver_id": [1001, 1002, 1003, 1004],
            "event_timestamp": [
                datetime(2021, 4, 12, 10, 59, 42),
                datetime(2021, 4, 12, 8, 12, 10),
                datetime(2021, 4, 12, 16, 40, 26),
                datetime(2021, 4, 12, 15, 1, 12),
            ],
        }
    )

    store = FeatureStore(repo_path=rpath)
    # get the feature service associated with this store
    feature_service = store.get_feature_service("driver_ranking_fv_svc")

    # Retrieve training data from local parquet FileSource
    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=feature_service
    ).to_df()

    return training_df


if __name__ == '__main__':
    tdf = get_training_data(Path("../"))
    pd.set_option('display.max_columns', 10)
    print(tdf.head())
    print(f"Training data shape: {tdf.shape}")