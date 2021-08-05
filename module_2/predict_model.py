import mlflow.sklearn 
import feast
import pandas as pd


class DriverRankingPredictModel:
    def __init__(self, repo_path, m_uri):
        # Load model from mlflow from the local model registry
        self._model = mlflow.sklearn.load_model(m_uri)

        # Set up feature store
        self._fs = feast.FeatureStore(repo_path=repo_path)

    def predict(self, driver_ids):
        # Read features from Feast
        driver_features = self._fs.get_online_features(
            entity_rows=[{"driver_id": driver_id} for driver_id in driver_ids],
            feature_refs=[
                "driver_hourly_stats:conv_rate",
                "driver_hourly_stats:acc_rate",
                "driver_hourly_stats:avg_daily_trips",
            ],
        )
        df = pd.DataFrame.from_dict(driver_features.to_dict())

        # Make prediction
        df["prediction"] = self._model.predict(df[sorted(df)])

        # Choose best driver
        best_driver_id = df["driver_id"].iloc[df["prediction"].argmax()]

        # return best driver
        return best_driver_id


if __name__ == "__main__":
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    REPO_PATH = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo"
    model_uri = "models:/sklearn_feast_integration/1"
    model = DriverRankingPredictModel(REPO_PATH, model_uri)
    drivers = [1001, 1002, 1003]
    best_driver = model.predict(drivers)
    print(f" Best predicted driver for completed trips: {best_driver}")