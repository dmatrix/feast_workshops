from feast import FeatureService
from features.feature_views import zipcode_features

# Define your feature service and the features it will serve
# FOR THE WORKSHOP LAB, UNCOMMENT THE LINES IN THIS FILE, STARTING BELOW
zipcode_features_svc = FeatureService(name="zipcode_features_svc",
                                      features=[zipcode_features],
                                      tags={"Description": "Used for training a XGBoost Logistic Regression model"})
