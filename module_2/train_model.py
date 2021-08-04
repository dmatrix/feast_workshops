import feast
from joblib import dump
import pandas as pd
from sklearn.linear_model import LinearRegression
import mlflow

if __name__ == '__main__':
    # Load driver order data
    orders = pd.read_csv("./data/driver_orders.csv", sep="\t")
    orders["event_timestamp"] = pd.to_datetime(orders["event_timestamp"])

    # Connect to your local feature store
    # change this to your location
    fs = feast.FeatureStore(repo_path="/Users/jules/git-repos/feast_workshops/module_1/feature_repo")

    # Retrieve training data from BigQuery
    training_df = fs.get_historical_features(
        entity_df=orders,
        feature_refs=[
            "driver_hourly_stats:conv_rate",
            "driver_hourly_stats:acc_rate",
            "driver_hourly_stats:avg_daily_trips",
        ],
    ).to_df()

    # Train model
    target = "trip_completed"

    # Enable autologging for mlflow
    mlflow.sklearn.autolog()
    reg = LinearRegression()
    train_X = training_df[training_df.columns.drop(target).drop("event_timestamp")]
    train_Y = training_df.loc[:, target]
    with mlflow.start_run() as run:
        reg.fit(train_X[sorted(train_X)], train_Y)
        mlflow.log_param("feast_data", "driver_hourly_stats")
        mlflow.log_dict({"features": ["driver_hourly_stats:conv_rate", "driver_hourly_stats:acc_rate", "driver_hourly_stats:avg_daily_trips"]}, "feast_data.json")
    print(f"model id: {run.info.run_id}")


