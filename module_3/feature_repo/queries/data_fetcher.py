import pandas as pd
from pathlib import Path

from feast import FeatureStore


class DataFetcher(object):
    def __init__(self, fs, rpath: Path, fsvc: str) -> None:
        self._fs = fs
        self._loan_data = rpath / "data" / "loan_table.parquet"
        self._fsvc = fsvc

    def get_loans_data(self) -> pd.DataFrame:
        return pd.read_parquet(self._loan_data)

    def get_online_data(self) -> pd.DataFrame:
        return pd.DataFrame()

    # Retrieve training data from local parquet FileSource
    # Use the loans data columns to enrich the features from FileSource
    def get_training_data(self) -> pd.DataFrame:
        loans_data = self.get_loans_data()
        fs_svc = self._fs.get_feature_service(self._fsvc)
        return self._fs.get_historical_features(
            entity_df=loans_data,
            features=fs_svc
        ).to_df()


if __name__ == "__main__":
    REPO_PATH = Path("/Users/jules/git-repos/feast_workshops/module_3/feature_repo")
    FEATURE_SVC = "zipcode_features_svc"
    store = FeatureStore(repo_path=REPO_PATH)
    fetcher = DataFetcher(store, REPO_PATH, FEATURE_SVC)
    df = fetcher.get_loans_data()
    print(df.head(3))
    print("--" * 5)
    training_df = fetcher.get_training_data()
    print(training_df)
