import sys
sys.path.insert(0, "../")

from datetime import datetime, timedelta
from pprint import pprint
from pathlib import Path
import pandas as pd

from feast import FeatureStore
from entities.entity import driver
from features.feature_views import driver_hourly_stats_view
from train import get_training_data
from fvector import get_feature_vector

FEAST_REPO = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo/"

if __name__ == "__main__":
    repo_path = Path(FEAST_REPO)
    fs = FeatureStore(repo_path=repo_path)

    # Register the data source, entity and features in the FeatureView with the Feast Registry
    fs.apply([driver, driver_hourly_stats_view])

    # get the training data
    training_df = get_training_data(repo_path)
    pd.set_option('display.max_columns', None)
    print(training_df.head())
    print(f"Training data shape: {training_df.shape}")

    # Now materialize data into online store
    fs.materialize_incremental(end_date=datetime.utcnow() - timedelta(minutes=5))

    # get the feature vector for inferencing from the online store
    feature_vector = get_feature_vector(repo_path)
    pprint(feature_vector)


