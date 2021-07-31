import pandas as pd
from datetime import datetime
from feast import FeatureStore

if __name__ == "__main__":
    # change this to your location
    FEAST_REPO = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo"
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

    store = FeatureStore(repo_path=FEAST_REPO)

    training_df = store.get_historical_features(
        entity_df=entity_df,
        feature_refs=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
        ],
    ).to_df()

    pd.set_option('display.max_columns', None)
    print(training_df.head())
    print(f"Training data shape: {training_df.shape}")