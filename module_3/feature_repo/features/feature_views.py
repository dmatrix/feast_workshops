# This is an example feature declaration file

from datetime import timedelta
from feast import Feature, FeatureView,  ValueType
from datasource.file_source import zipcode_batch_source, credit_history_source

# FOR THE WORKSHOP LAB, UNCOMMENT THE LINES IN THIS FILE, STARTING BELOW
zipcode_features = FeatureView(
    name="zipcode_features",
    entities=["zipcode"],
    ttl=timedelta(days=3650),
    features=[
        Feature(name="city", dtype=ValueType.STRING),
        Feature(name="state", dtype=ValueType.STRING),
        Feature(name="location_type", dtype=ValueType.STRING),
        Feature(name="tax_returns_filed", dtype=ValueType.INT64),
        Feature(name="population", dtype=ValueType.INT64),
        Feature(name="total_wages", dtype=ValueType.INT64),
    ],
    batch_source=zipcode_batch_source,
    online=True,
)

credit_history = FeatureView(
    name="credit_history",
    entities=["dob_ssn"],
    ttl=timedelta(days=90),
    features=[
        Feature(name="credit_card_due", dtype=ValueType.INT64),
        Feature(name="mortgage_due", dtype=ValueType.INT64),
        Feature(name="student_loan_due", dtype=ValueType.INT64),
        Feature(name="vehicle_loan_due", dtype=ValueType.INT64),
        Feature(name="hard_pulls", dtype=ValueType.INT64),
        Feature(name="missed_payments_2y", dtype=ValueType.INT64),
        Feature(name="missed_payments_1y", dtype=ValueType.INT64),
        Feature(name="missed_payments_6m", dtype=ValueType.INT64),
        Feature(name="bankruptcies", dtype=ValueType.INT64),
    ],
    batch_source=credit_history_source,
    online=True
)