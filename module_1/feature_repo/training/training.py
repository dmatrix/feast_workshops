import pandas as pd
from fsutils import create_entity_df, get_training_data

if __name__ == "__main__":
    # change this to your location
    FEAST_REPO = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo"
    # list of drivers for whom you want to create an entity dataframe
    drivers = [1001, 1002, 1003]
    entity_df = create_entity_df(drivers)
    # Fetch the training data set composed of all rows that make up the entity data frame
    df = get_training_data(FEAST_REPO, entity_df)
    pd.set_option('display.max_columns', None)
    print(df.head())