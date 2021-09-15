import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import precision_score


import xgboost as xgb

from feast import FeatureStore
from data_fetcher import DataFetcher


class CreditXGBClassifier:

    target = "loan_status"

    categorical_features = [
        "person_home_ownership",
        "loan_intent",
        "city",
        "state",
        "location_type",
    ]

    columns_to_drop = [
        "event_timestamp",
        "created_timestamp",
        "loan_id",
        "loan_status",
        "dob_ssn",
    ]

    zipcode_features = [
        "zipcode_features:city",
        "zipcode_features:state",
        "zipcode_features:location_type",
        "zipcode_features:tax_returns_filed",
        "zipcode_features:population",
        "zipcode_features:total_wages",
    ]

    def __init__(self, fs, data_fetcher):
        self._fs = fs
        self._data_fetcher = data_fetcher

        self._encoder = OrdinalEncoder()

        # Drop the unneeded columns
        self._training_df = data_fetcher.get_training_data()
        self._apply_ordinal_encoding(self._training_df)
        self._train_y = self._training_df[self.target]
        self._train_X = self._training_df.drop(columns=self.columns_to_drop)
        self._train_X = self._train_X.reindex(sorted(self._train_X.columns), axis=1)
        self._trained_model = None

        # Create an instance of the classifier
        self._model = xgb.XGBClassifier()

    def _apply_ordinal_encoding(self, data):
        data[self.categorical_features] = self._encoder.fit_transform(
            data[self.categorical_features])

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

        # use DMatrix for xgboost
        dtrain = xgb.DMatrix(data=X_train, label=y_train, enable_categorical=True)
        dtest = xgb.DMatrix(data=X_test, label=y_test, enable_categorical=True)

        # Set xgboost params

        param = {
            'max_depth': 3,  # the maximum depth of each tree
            'eta': 0.3,  # the training step for each iteration
            'objective': 'binary:logistic',  # error evaluation for binary class training
            'num_class': 1 # the number of classes that exist in this datset
        }

        num_round = 20  # the number of training iterations

        # training and testing - numpy matrices
        bst = xgb.train(param, dtrain, num_round)
        preds = bst.predict(dtest)

        # save the trained model
        self._trained_model = bst

        # extracting most confident predictions
        best_preds = np.asarray([np.argmax(line) for line in preds])
        print(f"Numpy array precision: {precision_score(y_test, best_preds, zero_division=1)}")

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
        data = xgb.DMatrix(features_df)
        features_df["prediction"] = self.trained_model.predict(data)

        # return result of credit scoring
        return features_df["prediction"].iloc[0]

    def _get_online_zipcode_features(self, request):
        zipcode = request["zipcode"][0]

        return self._fs.get_online_features(
            entity_rows=[{"zipcode": zipcode}], features=self.zipcode_features
        ).to_dict()


if __name__ == '__main__':
    REPO_PATH = Path("/Users/jules/git-repos/feast_workshops/module_3/feature_repo")
    store = FeatureStore(repo_path=REPO_PATH)
    fetcher = DataFetcher(store, REPO_PATH)
    xgboost_cls = CreditXGBClassifier(store, fetcher)
    pd.set_option('display.max_columns', 50)
    print(xgboost_cls.training_df.head(3))
    print(type(xgboost_cls.model))

    xgboost_cls.train()

    loan_request = {
        "zipcode": [76104],
        "person_age": [133],
        "person_income": [59000],
        "person_home_ownership": ["RENT"],
        "person_emp_length": [123.0],
        "loan_intent": ["PERSONAL"],
        "loan_amnt": [35000],
        "loan_int_rate": [16.02],
    }

    result = xgboost_cls.predict(loan_request)
    print(f"Loan approved: {result}")

