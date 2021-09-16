from dataclasses import dataclass


@dataclass
class FeatureData:

    def __init__(self):
        self.target = "loan_status"
        self.categorical_features = [
            "person_home_ownership",
            "loan_intent",
            "city",
            "state",
            "location_type",
            "dob_ssn",
        ]
        self.columns_to_drop = [
            "event_timestamp",
            "created_timestamp",
            "loan_id",
            "loan_status",
        ]
        self.zipcode_features = [
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


if __name__ == '__main__':
    data_cls = FeatureData()
    print(data_cls.zipcode_features)