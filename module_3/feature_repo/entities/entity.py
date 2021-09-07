# Declare our Feast Entity around which we want to index to build augmented
# Features from another source such as a file or a table

# FOR THE WORKSHOP LAB, UNCOMMENT THE LINES IN THIS FILE, STARTING BELOW
from feast import Entity, ValueType

zipcode = Entity(
    name="zipcode",
    value_type=ValueType.INT64,
    description="Zipcode for the loan origin"
)

dob_ssn = Entity(
    name="dob_ssn",
    value_type=ValueType.STRING,
    description="Date of birth and last four digits of social security number"
)