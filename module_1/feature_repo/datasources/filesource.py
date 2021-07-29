# This is an example definition file for data source FileSource

import feast as fst

# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite DWH, such as BigQuery. See Feast documentation
# for more info.
driver_hourly_stats = fst.FileSource(
    path="/Users/jules/git-repos/feature_repo/data/driver_stats.parquet",
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)
