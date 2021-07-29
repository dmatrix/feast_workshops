# This is an example entity definition for an Entity

import feast as fst

# Define an entity for the driver. You can think of entity as a primary key used to
# fetch features.
driver = fst.Entity(name="driver_id", value_type=fst.ValueType.INT64, description="driver id",)
