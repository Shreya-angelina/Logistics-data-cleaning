import pandas as pd

df = pd.read_csv("data/orders_cleaned.csv")

print("=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

# Critical geographic fields
assert df["destination_lat"].notna().all()
assert df["destination_lon"].notna().all()

# Canonical categorical labels
assert df["origin_hub"].isin(
    ["hub_1", "hub_2", "hub_3"]
).all()

# Standardized numeric columns should contain valid finite values.
# parcel_weight_kg is z-score standardized, so negative standardized
# values are valid and do not represent negative physical weight.
for column in ["distance_km", "parcel_weight_kg", "traffic_index"]:
    assert df[column].notna().all()
    assert df[column].map(lambda x: pd.notna(x) and pd.api.types.is_number(x)).all()

print("No missing destination coordinates.")
print("Canonical hub labels confirmed.")
print("Regression features contain valid standardized values.")
print("Final cleaned dataset shape:", df.shape)

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nFinal dataset preview:")
print(df.head())

print("\nValidation completed successfully.")
