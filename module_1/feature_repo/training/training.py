import pandas as pd
from fsutils import create_entity_df, get_training_data

if __name__ == "__main__":
    FEAST_REPO = "/Users/jules/git-repos/feature_repo"
    drivers = [1001, 1002, 1003, 1004]
    entity_df = create_entity_df(drivers)
    df = get_training_data(FEAST_REPO, entity_df)
    pd.set_option('display.max_columns', None)
    print(df.head())


