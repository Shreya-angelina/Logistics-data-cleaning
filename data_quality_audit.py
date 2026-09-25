import pandas as pd

df = pd.read_csv(
    "data/collected_logistics_data.csv",
    parse_dates=["order_time", "delivery_time", "order_date"]
)

print("=" * 60)
print("DATA QUALITY AUDIT")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate order IDs:")
print(df["order_id"].duplicated().sum())

print("\nNumerical summary:")
print(df.describe())

print("\nOrigin hub labels:")
print(df["origin_hub"].value_counts(dropna=False))

print("\nDelivery status labels:")
print(df["delivery_status"].value_counts(dropna=False))

print("\nInvalid distance values:")
print(((df["distance_km"] <= 0) | (df["distance_km"] > 500)).sum())

print("\nInvalid parcel weights:")
print((df["parcel_weight_kg"] <= 0).sum())
