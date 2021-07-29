# This is an example feature definition file
import feast as fst

from datasources.filesource import driver_hourly_stats

from google.protobuf.duration_pb2 import Duration

# Our parquet files contain sample data that includes a driver_id column, timestamps and
# three feature column. Here we define a Feature View that will allow us to serve this
# data to our model online.
driver_hourly_stats_view = fst.FeatureView(
    name="driver_hourly_stats",
    entities=["driver_id"],
    ttl=Duration(seconds=86400 * 1),
    features=[
        fst.Feature(name="conv_rate", dtype=fst.ValueType.FLOAT),
        fst.Feature(name="acc_rate", dtype=fst.ValueType.FLOAT),
        fst.Feature(name="avg_daily_trips", dtype=fst.ValueType.INT64),
    ],
    online=True,
    input=driver_hourly_stats,
    tags={},
)
