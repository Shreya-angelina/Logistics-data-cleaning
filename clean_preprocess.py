import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

df = pd.read_csv(
    "data/collected_logistics_data.csv",
    parse_dates=["order_time", "delivery_time", "order_date"]
)

# ---------------------------------------------------------
# 1. Remove duplicate orders
# ---------------------------------------------------------
print("Duplicates found:", df.duplicated(subset="order_id").sum())

df = df.drop_duplicates(
    subset="order_id",
    keep="first"
)

# ---------------------------------------------------------
# 2. Standardize categorical labels
# ---------------------------------------------------------
df["origin_hub"] = (
    df["origin_hub"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["delivery_status"] = (
    df["delivery_status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

hub_map = {
    "hub 1": "hub_1",
    "h1": "hub_1",
    "hub1": "hub_1",
    "hub 2": "hub_2",
    "h2": "hub_2",
    "hub2": "hub_2",
    "hub 3": "hub_3",
    "h3": "hub_3",
    "hub3": "hub_3"
}

df["origin_hub"] = df["origin_hub"].replace(hub_map)

# ---------------------------------------------------------
# 3. Handle missing values
# ---------------------------------------------------------

# Do not create a fake delivery time for cancelled orders
df["is_cancelled"] = df["delivery_status"].eq("cancelled")

# Create hour-of-day feature
df["order_hour"] = df["order_time"].dt.hour

# Median traffic imputation by hub and hour
df["traffic_index"] = df.groupby(
    ["origin_hub", "order_hour"]
)["traffic_index"].transform(
    lambda s: s.fillna(s.median())
)

# Fallback median if a hub/hour group is entirely missing
df["traffic_index"] = df["traffic_index"].fillna(
    df["traffic_index"].median()
)

# Destination coordinates cannot be meaningfully fabricated
df = df.dropna(
    subset=["destination_lat", "destination_lon"]
)

# ---------------------------------------------------------
# 4. Outlier detection using IQR
# ---------------------------------------------------------
def iqr_bounds(series, k=1.5):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

low, high = iqr_bounds(df["distance_km"])

outlier_mask = (
    (df["distance_km"] < max(low, 0))
    | (df["distance_km"] > high)
)

print("Distance outliers flagged:", outlier_mask.sum())

df = df[~outlier_mask]

# Remove non-physical parcel weights
df = df[df["parcel_weight_kg"] > 0]

# ---------------------------------------------------------
# 5. Feature scaling
# ---------------------------------------------------------

# Min-Max scaling for clustering features
cluster_features = [
    "destination_lat",
    "destination_lon"
]

minmax_scaler = MinMaxScaler()

df[cluster_features] = minmax_scaler.fit_transform(
    df[cluster_features]
)

# Z-score standardization for regression features
reg_features = [
    "distance_km",
    "parcel_weight_kg",
    "traffic_index"
]

standard_scaler = StandardScaler()

df[reg_features] = standard_scaler.fit_transform(
    df[reg_features]
)

df.to_csv(
    "data/orders_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved to data/orders_cleaned.csv")
print("Final shape:", df.shape)
