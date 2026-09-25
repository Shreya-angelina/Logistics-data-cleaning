import pandas as pd

# Simulated collection from OMS, GPS/telematics and WMS
orders = pd.read_csv(
    "data/orders.csv",
    parse_dates=["order_time", "delivery_time"]
)

telemetry = pd.read_csv(
    "data/vehicle_telemetry.csv"
)

warehouse = pd.read_csv(
    "data/warehouse_inventory.csv",
    parse_dates=["order_date"]
)

# Derive order_date for the warehouse join
orders["order_date"] = orders["order_time"].dt.normalize()

# Join the three operational sources
df = orders.merge(
    telemetry,
    on="order_id",
    how="left",
    suffixes=("", "_telemetry")
)

# Use the telemetry traffic index where available
if "traffic_index_telemetry" in df.columns:
    df["traffic_index"] = df["traffic_index_telemetry"]
    df.drop(columns=["traffic_index_telemetry"], inplace=True)

df = df.merge(
    warehouse,
    on=["origin_hub", "order_date"],
    how="left"
)

print("Combined dataset shape:", df.shape)
print("\nData types:")
print(df.dtypes)

df.to_csv("data/collected_logistics_data.csv", index=False)
print("\nSaved: data/collected_logistics_data.csv")
