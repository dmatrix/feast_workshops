import pandas as pd
from pathlib import Path
from pprint import pprint

from feast import FeatureStore


class DataFetcher(object):
    feast_features = [
        "zipcode_features:city",
        "zipcode_features:state",
        "zipcode_features:location_type",
        "zipcode_features:tax_returns_filed",
        "zipcode_features:population",
        "zipcode_features:total_wages",
        "credit_history:credit_card_due",
        "credit_history:mortgage_due",
        "credit_history:student_loan_due",
        "credit_history:vehicle_loan_due",
        "credit_history:hard_pulls",
        "credit_history:missed_payments_2y",
        "credit_history:missed_payments_1y",
        "credit_history:missed_payments_6m",
        "credit_history:bankruptcies",
    ]

    def __init__(self, fs, rpath: Path) -> None:
        self._fs = fs
        self._loan_data = rpath / "data" / "loan_table.parquet"

    def get_loans_data(self) -> pd.DataFrame:
        return pd.read_parquet(self._loan_data)

    def get_online_data(self, zipcode: int, dob_ssn: str) -> dict:
        return self._fs.get_online_features(
            entity_rows=[{"zipcode": zipcode, "dob_ssn": dob_ssn}],
            features=self.feast_features
        ).to_dict()

    # Retrieve training data from local parquet FileSource
    # Use the loans data columns to enrich the features from FileSource
    def get_training_data(self) -> pd.DataFrame:
        loans_data = self.get_loans_data()
        return self._fs.get_historical_features(
            entity_df=loans_data,
            features=self.feast_features
        ).to_df()


if __name__ == "__main__":
    REPO_PATH = Path("/Users/jules/git-repos/feast_workshops/module_3/feature_repo")
    store = FeatureStore(repo_path=REPO_PATH)
    fetcher = DataFetcher(store, REPO_PATH)

    # Get loan data to enrich our historical zipcode features
    pd.set_option('display.max_columns', 50)
    df = fetcher.get_loans_data()
    print(" Loans Data")
    print("--" * 5)
    print(df.head(3))
    print(df.columns)
    print("--" * 5)

    # Get training data: zipcode features + load data
    training_df = fetcher.get_training_data()
    print(" Training Data")
    print("--" * 5)
    print(training_df.head(3))
    print(training_df.columns)
    print("--" * 5)

    # Get online vector data for specific zipcode
    zipcodes_dob_ssns = [(30721, "19790429_9552"), (48893, "19971025_8002")]
    for zipcode, dob_ssn in zipcodes_dob_ssns:
        print(f"Fetching feature vector for zipcode and dob_ssn:{zipcode}, {dob_ssn}")
        data = fetcher.get_online_data(zipcode, dob_ssn)
        pprint(data)

