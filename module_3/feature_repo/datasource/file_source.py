# This is an example of data source declaration file
from feast import FileSource

# Read data from parquet files. Parquet is convenient for local development mode. For production, you can
# use your favorite data warehouse (DWH), such as BigQuery or AWS Redshift. See Feast documentation for more info.

# Change path to your location in the feast repo for module 3
# FOR THE WORKSHOP LAB, UNCOMMENT THE LINES IN THIS FILE, STARTING BELOW
zipcode_batch_source = FileSource(path="/Users/jules/git-repos/feast_workshops/module_3/feature_repo/data/zipcode_table.parquet",
                                 event_timestamp_column="datetime",
                                 created_timestamp_column="created")