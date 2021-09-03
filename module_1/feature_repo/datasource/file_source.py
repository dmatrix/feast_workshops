# This is an example of data source declaration file
from feast import FileSource

# Read data from parquet files. Parquet is convenient for local development mode. For production, you can 
# use your favorite data warehouse (DWH), such as BigQuery or AWS Redshift. See Feast documentation for more info.

# change path to your location in the repo
driver_hourly_stats = FileSource(path="/Users/jules/git-repos/feature_repo/data/driver_stats.parquet",
                                 event_timestamp_column="datetime",
                                 created_timestamp_column="created")
