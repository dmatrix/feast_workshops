import pandas as pd
import time
import timeit
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import precision_score

from xgboost_ray import RayXGBClassifier, RayParams
import xgboost as xgb

from feast import FeatureStore
import sys

sys.path.insert(0, "../")

from utils.data_fetcher import DataFetcher
from utils.feature_data import FeatureData


class CreditRayXGBClassifier:

    def __init__(self, fs, data_fetcher):
        self._fs = fs
        self._data_fetcher = data_fetcher
        self._encoder = OrdinalEncoder()
        self._data_cls = FeatureData()

        self._training_df = data_fetcher.get_training_data()
        self._apply_ordinal_encoding(self._training_df)
        self._train_y = self._training_df[self._data_cls.target]

        # Drop the unneeded columns
        self._train_X = self._training_df.drop(columns=self._data_cls.columns_to_drop)
        self._train_X = self._train_X.reindex(sorted(self._train_X.columns), axis=1)
        self._trained_model = None

        # Create an instance of the classifier
        self._model = RayXGBClassifier(
                    n_jobs=4,  # In XGBoost-Ray, n_jobs sets the number of actors
                    random_state=42
        )

    def _apply_ordinal_encoding(self, data):
        data[self._data_cls.categorical_features] = self._encoder.fit_transform(
            data[self._data_cls.categorical_features])

    @property
    def training_df(self) -> pd.DataFrame:
        return self._training_df

    @property
    def model(self):
        return self._model

    @property
    def trained_model(self):
        return self._trained_model

    @property
    def train_y(self) ->pd.DataFrame:
        return self._train_y

    @property
    def train_X(self) -> pd.DataFrame:
        return self._train_X

    def train(self) -> None:

        X_train, X_test, y_train, y_test = train_test_split(self._train_X, self._train_y, random_state=42)

        # training and testing - numpy matrices
        bst = self._model.fit(X_train, y_train)

        pred_ray = bst.predict(X_test)
        print(pred_ray)

        # save the trained model
        self._trained_model = bst

    def predict(self, request):
        # Get Zipcode features from Feast
        zipcode_features = self._get_online_zipcode_features(request)

        # Join features to request features
        features = request.copy()
        features.update(zipcode_features)
        features_df = pd.DataFrame.from_dict(features)

        # Sort columns
        features_df = features_df.reindex(sorted(features_df.columns), axis=1)

        # Apply ordinal encoding to categorical features
        self._apply_ordinal_encoding(features_df)

        # Make prediction
        features_df["prediction"] = self.trained_model.predict(features_df, ray_params=RayParams(num_actors=1))

        # return result of credit scoring
        return features_df["prediction"].iloc[0]

    def _get_online_zipcode_features(self, request):
        zipcode = request["zipcode"][0]
        dob_ssn = request["dob_ssn"][0]

        return self._fs.get_online_features(
            entity_rows=[{"zipcode": zipcode, "dob_ssn": dob_ssn}], features=self._data_cls.zipcode_features
        ).to_dict()


if __name__ == '__main__':
    REPO_PATH = Path("/Users/jules/git-repos/feast_workshops/module_3/feature_repo")
    store = FeatureStore(repo_path=REPO_PATH)
    fetcher = DataFetcher(store, REPO_PATH)
    xgboost_cls = CreditRayXGBClassifier(store, fetcher)

    start = time.time()
    # Train the model
    xgboost_cls.train()

    loan_requests = [
        {
            "zipcode": [76104],
            "person_age": [22],
            "person_income": [59000],
            "person_home_ownership": ["RENT"],
            "person_emp_length": [123.0],
            "loan_intent": ["PERSONAL"],
            "loan_amnt": [35000],
            "loan_int_rate": [16.02],
            "dob_ssn": ["19530219_5179"]
        },
        {
            "zipcode": [69033],
            "person_age": [66],
            "person_income": [42000],
            "person_home_ownership": ["RENT"],
            "person_emp_length": [2.0],
            "loan_intent": ["MEDICAL"],
            "loan_amnt": [6475],
            "loan_int_rate": [9.99],
            "dob_ssn": ["19960703_3449"]
        }
    ]

    # Now do the predictions
    for loan_request in loan_requests:
        result = round(xgboost_cls.predict(loan_request))
        loan_status = "approved" if result == 1 else "rejected"
        print(f"Loan for {loan_request['zipcode'][0]} code {loan_status}: status_code={result}")

    elapsed = round(time.time() - start)
    print(f"Total time elapsed: {elapsed} sec")