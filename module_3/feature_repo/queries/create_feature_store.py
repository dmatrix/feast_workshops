import sys
sys.path.insert(0, "../")

from datetime import datetime
from pathlib import Path
import pandas as pd

from feast import FeatureStore
from entities.entity import zipcode
from features.feature_views import zipcode_features
from feature_service.feature_svc import zipcode_features_svc
from data_fetcher import DataFetcher


# Change this location to yours
FEAST_REPO = "/Users/jules/git-repos/feast_workshops/module_3/feature_repo/"

if __name__ == "__main__":
    repo_path = Path(FEAST_REPO)
    fs = FeatureStore(repo_path=repo_path)

    # Step 1. Register the data source, entity, features and feature service in the FeatureView with the Feast Registry
    fs.apply([zipcode, zipcode_features_svc, zipcode_features])

    # Step 2. Now materialize, load data into online store
    fs.materialize_incremental(end_date=datetime.utcnow())
