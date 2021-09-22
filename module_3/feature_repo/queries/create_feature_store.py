import sys
sys.path.insert(0, "../")

from datetime import datetime
from pathlib import Path
import pandas as pd
from pprint import pprint

from feast import FeatureStore
from entities.entity import zipcode, dob_ssn
from features.feature_views import zipcode_features, credit_history
from feature_service.feature_svc import zipcode_features_svc
from utils.data_fetcher import DataFetcher

# Change this location to yours
FEAST_REPO = "/Users/jsd/git-repos/feast_workshops/module_3/feature_repo/"

if __name__ == "__main__":
    repo_path = Path(FEAST_REPO)
    fs = FeatureStore(repo_path=repo_path)

    # Step 1. Register the data source, entity, features and feature service in the FeatureView with the Feast Registry
    fs.apply([zipcode, dob_ssn, zipcode_features, credit_history, zipcode_features_svc])

    # Step 2. Now materialize, load data into online store
    fs.materialize_incremental(end_date=datetime.utcnow())

    # Step 3. Fetch training data augmented with loans data
    fetcher = DataFetcher(fs, repo_path)
    training_df = fetcher.get_training_data()
    print(" Training Data --- ")
    print(training_df.head(3))
    print(training_df.columns)
    print("--" * 5)

    # Step 4. Get some inference data for zipcode
    zipcodes_dob_ssns = [(30721, "19790429_9552"), (48893, "19971025_8002")]
    for zipcode, dob_ssn in zipcodes_dob_ssns:
        print(f"Fetching feature vector for zipcode and dob_ssn:{zipcode}, {dob_ssn}")
        data = fetcher.get_online_data(zipcode, dob_ssn)
        pprint(data)
