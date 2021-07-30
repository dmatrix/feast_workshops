# This is an example definition file for data source FileSource

import feast as fst

# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite data warehouse (DWH), such as BigQuery, Redshift
# or Snowflake. See Feast documentation for more info on supported external data sources

# define the driver_hourly_stats as your data source
driver_hourly_stats = fst.FileSource(
    # change this to your location
    path="/Users/jules/git-repos/feast_workshops/module_1/feature_repo/data/driver_stats.parquet",
    # the timestamp when this event occurred
    event_timestamp_column="datetime",
    # timestamp when it was registered
    created_timestamp_column="created",
)
