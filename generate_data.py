import numpy as np
import pandas as pd

# Simulate approximately 45,000 logistics delivery records
np.random.seed(42)
N = 45000

order_id = [f"ORD{100000+i}" for i in range(N)]
dates = pd.date_range("2025-01-01", periods=180, freq="h")
order_time = np.random.choice(dates, N)

origin_hub = np.random.choice(["Hub 1", "Hub 2", "Hub 3"], N)
destination_lat = np.random.uniform(12.85, 13.20, N)
destination_lon = np.random.uniform(80.05, 80.35, N)

distance_km = np.random.gamma(shape=3.0, scale=8.0, size=N)
distance_km = np.clip(distance_km, 1, 80)

parcel_weight_kg = np.random.gamma(shape=2.5, scale=2.0, size=N)
parcel_weight_kg = np.clip(parcel_weight_kg, 0.1, 25)

vehicle_id = np.random.choice(
    [f"V{i:03d}" for i in range(1, 101)], N
)

traffic_index = np.clip(np.random.beta(4, 3, N), 0, 1)

delivery_status = np.random.choice(
    ["On-time", "Late", "Cancelled"],
    N,
    p=[0.78, 0.17, 0.05]
)

delivery_hours = (
    0.5
    + distance_km / 25
    + parcel_weight_kg / 20
    + traffic_index * 2
    + np.random.normal(0, 0.5, N)
)
delivery_hours = np.maximum(delivery_hours, 0.2)

delivery_time = (
    pd.Series(order_time)
    + pd.to_timedelta(delivery_hours, unit="h")
)

# Missing delivery time for cancelled orders
delivery_time = pd.Series(delivery_time)
delivery_time[delivery_status == "Cancelled"] = pd.NaT

orders = pd.DataFrame({
    "order_id": order_id,
    "order_time": order_time,
    "delivery_time": delivery_time,
    "origin_hub": origin_hub,
    "destination_lat": destination_lat,
    "destination_lon": destination_lon,
    "distance_km": distance_km,
    "parcel_weight_kg": parcel_weight_kg,
    "vehicle_id": vehicle_id,
    "delivery_status": delivery_status
})

# Introduce realistic data-quality problems described in the report
orders.loc[np.random.choice(N, 120, replace=False), "destination_lat"] = np.nan
orders.loc[np.random.choice(N, 120, replace=False), "destination_lon"] = np.nan

orders.loc[np.random.choice(N, 40, replace=False), "distance_km"] = 0
orders.loc[np.random.choice(N, 25, replace=False), "distance_km"] = 600
orders.loc[np.random.choice(N, 20, replace=False), "parcel_weight_kg"] = -2

# Categorical label variants
idx = np.random.choice(N, 300, replace=False)
orders.loc[idx[:100], "origin_hub"] = "H1"
orders.loc[idx[100:200], "origin_hub"] = "hub1"
orders.loc[idx[200:], "origin_hub"] = "Hub 2"

idx = np.random.choice(N, 250, replace=False)
orders.loc[idx[:80], "delivery_status"] = "late"
orders.loc[idx[80:160], "delivery_status"] = "LATE"
orders.loc[idx[160:], "delivery_status"] = "late "

# Duplicate some order records
duplicates = orders.sample(150, random_state=42)
orders_with_duplicates = pd.concat(
    [orders, duplicates],
    ignore_index=True
)

# Vehicle telemetry table
telemetry = pd.DataFrame({
    "order_id": orders["order_id"],
    "vehicle_id": orders["vehicle_id"],
    "traffic_index": traffic_index
})

# Simulate telemetry outages
missing_idx = np.random.choice(N, 700, replace=False)
telemetry.loc[missing_idx, "traffic_index"] = np.nan

# Warehouse inventory table
warehouse_dates = pd.date_range("2025-01-01", periods=180, freq="D")
warehouse = pd.DataFrame({
    "origin_hub": np.tile(["Hub 1", "Hub 2", "Hub 3"], 180),
    "order_date": np.repeat(warehouse_dates, 3),
    "inventory_units": np.random.randint(1000, 10000, 540)
})

orders_with_duplicates.to_csv(
    "data/orders.csv", index=False
)
telemetry.to_csv(
    "data/vehicle_telemetry.csv", index=False
)
warehouse.to_csv(
    "data/warehouse_inventory.csv", index=False
)

print("Generated:")
print("  data/orders.csv")
print("  data/vehicle_telemetry.csv")
print("  data/warehouse_inventory.csv")
print("Rows in orders:", len(orders_with_duplicates))
