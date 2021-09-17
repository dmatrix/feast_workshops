# This is an example feature definition file
# See documentation: https://rtd.feast.dev/en/latest/#module-feast.entity

from feast import Entity, ValueType

# Define an entity for the driver. You can think of entity as a primary key used to
# fetch or build features around.
driver = Entity(name="driver_id", value_type=ValueType.INT64, description="driver id",)
