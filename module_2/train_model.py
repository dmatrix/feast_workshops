import pandas as pd
from pprint import pprint
from sklearn.linear_model import ElasticNet
import feast
import mlflow


class DriverRankingTrainModel:
    def __init__(self, repo_path: str, f_service_name: str, tuning_params={}) -> None:
        self._repo_path = repo_path
        self._params = tuning_params
        self._feature_service_name = f_service_name

    def get_training_data(self) -> pd.DataFrame:

        # Load driver order data
        orders = pd.read_csv("./data/driver_orders.csv", sep="\t")
        orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])

        # Connect to your local feature store
        # change this to your location
        store = feast.FeatureStore(repo_path=self._repo_path)
        feature_service = store.get_feature_service(self._feature_service_name )

        # Retrieve training data from local parquet FileSource
        training_df = store.get_historical_features(
            entity_df=orders,
            features=feature_service
        ).to_df()
        
        return training_df

    def train_model(self) -> str:
        # Enable autologging for mlflow and set the tracking uri with the local model registry
        # SQLite db
        mlflow.set_tracking_uri("sqlite:///mlruns.db")
        mlflow.sklearn.autolog()

        # create model
        model = ElasticNet(**self._params)
        target = "trip_completed"
        training_df = self.get_training_data()
        train_X = training_df[training_df.columns.drop(target).drop("event_timestamp")]
        train_y = training_df.loc[:, target]

        # log some parameters and Feast feature names
        with mlflow.start_run() as run:
            model.fit(train_X[sorted(train_X)], train_y)
            mlflow.log_param("feast_data", "driver_hourly_stats")
            mlflow.log_dict({"features": ["driver_hourly_stats:conv_rate", "driver_hourly_stats:acc_rate",
                                          "driver_hourly_stats:avg_daily_trips"]}, "feast_data.json")
        return {run.info.run_id}


if __name__ == '__main__':
    REPO_PATH = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo"
    FEATURE_SERVICE_NAME = "driver_ranking_fv_svc"
    params_list = [{"alpha": 0.5, "l1_ratio": 0.15},
                   {"alpha": 0.75, "l1_ratio": 0.25},
                   {"alpha": 1.0, "l1_ratio": 0.5}]
    # iterate over tuning parameters
    for params in params_list:
        model_cls = DriverRankingTrainModel(REPO_PATH, FEATURE_SERVICE_NAME, params)
        run_id = model_cls.train_model()
        pprint(f"ElasticNet params: {params}")
        print(f"Model run id: {run_id}")


