import pandas as pd
from pathlib import Path
from pprint import pprint

from feast import FeatureStore

zipcode_features = [
        "zipcode_features:city",
        "zipcode_features:state",
        "zipcode_features:location_type",
        "zipcode_features:tax_returns_filed",
        "zipcode_features:population",
        "zipcode_features:total_wages",
    ]


class DataFetcher(object):
    def __init__(self, fs, rpath: Path, fsvc: str) -> None:
        self._fs = fs
        self._loan_data = rpath / "data" / "loan_table.parquet"
        self._fsvc = fsvc

    def get_loans_data(self) -> pd.DataFrame:
        return pd.read_parquet(self._loan_data)

    def get_online_data(self, zcode: int) -> dict:
        return self._fs.get_online_features(
            entity_rows=[{"zipcode": zcode}],
            features=zipcode_features
        ).to_dict()

    # Retrieve training data from local parquet FileSource
    # Use the loans data columns to enrich the features from FileSource
    def get_training_data(self) -> pd.DataFrame:
        loans_data = self.get_loans_data()
        fs_svc = self._fs.get_feature_service(self._fsvc)
        return self._fs.get_historical_features(
            entity_df=loans_data,
            features=zipcode_features
        ).to_df()


if __name__ == "__main__":
    REPO_PATH = Path("/Users/jules/git-repos/feast_workshops/module_3/feature_repo")
    FEATURE_SVC = "zipcode_features_svc"
    store = FeatureStore(repo_path=REPO_PATH)
    fetcher = DataFetcher(store, REPO_PATH, FEATURE_SVC)

    # Get loan data to enrich our historical zipcode features
    df = fetcher.get_loans_data()
    print(df.head(3))
    print(df.columns)
    print("--" * 5)

    # Get training data: zipcode features + load data
    training_df = fetcher.get_training_data()
    print(training_df.head(3))
    print(training_df.columns)
    print("--" * 5)

    # Get online vector data for specific zipcode
    zipcodes = [55738, 17748, 72944]
    for zipcode in zipcodes:
        print(f"Fetching feature vector for zipcode:{zipcode}")
        data = fetcher.get_online_data(zipcode)
        pprint(data)

