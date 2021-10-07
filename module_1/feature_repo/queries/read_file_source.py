import pandas as pd

if __name__ == '__main__':
    DATA_SOURCE_FILE = "/Users/jules/git-repos/feast_workshops/module_1/feature_repo/data/driver_stats.parquet"
    df = pd.read_parquet(DATA_SOURCE_FILE)
    pd.set_option('display.max_columns', 10)
    print(df.head(2))
    print(f"Data Source Parquet Shape={df.shape}")
    print(f"columns={df.columns}")
