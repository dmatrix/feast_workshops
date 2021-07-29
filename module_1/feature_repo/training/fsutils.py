from datetime import datetime
import pandas as pd
import feast as fst

def create_entity_df(drivers: list) -> pd.DataFrame:
    """
    Create an entity dataframe to be joined with in the Entity rows in the offline store.
    In this case, the offline store is our data/driver_stats.parquet file
    """
    entity_df = pd.DataFrame.from_dict(
        {
            "driver_id": drivers,
            "event_timestamp": [
            datetime(2021, 4, 12, 10, 59, 42),
            datetime(2021, 4, 12, 8, 12, 10),
            datetime(2021, 4, 12, 16, 40, 26),
            datetime(2021, 4, 12, 15, 1, 12),
        ],
        }
    )
    return entity_df


def get_training_data(repo_path: str, edf: list[str]) -> pd.DataFrame:
    """
    Fetch historical features from the offline feature store
    """
    store = fst.FeatureStore(repo_path=repo_path)
    training_df = store.get_historical_features(
        entity_df=edf,
        feature_refs=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
        ],
    ).to_df()
    return training_df


def get_online_data(repo_path: str, id: int) -> dict:
    """
    Fetch feature vector for fo inferencing
    """
    store= fst.FeatureStore(repo_path=repo_path)
    feature_vector = store.get_online_features(
        feature_refs=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
        ],
        entity_rows=[{"driver_id": id}],
    ).to_dict()

    return feature_vector


