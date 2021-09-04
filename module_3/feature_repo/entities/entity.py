# Declare our Feast Entity around which we want to index to build augmented
# Features from another source such as a file or a table

# FOR THE WORKSHOP LAB, UNCOMMENT THE LINES IN THIS FILE, STARTING BELOW
from feast import Entity, ValueType

zipcode = Entity(name="zipcode", value_type=ValueType.INT64)