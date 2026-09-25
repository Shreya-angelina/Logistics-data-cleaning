# Week 2 – Data Collection, Cleaning & Preprocessing for Logistics Analysis

This repository contains the Python programs for the Week 2 Northbridge Logistics task.

## Objective

Build a reliable data pipeline that simulates data collection from order-management, GPS/telematics and warehouse systems, identifies data-quality problems, cleans the data, performs preprocessing, and validates the final analysis-ready dataset.

## Program Files

- `generate_data.py` – Creates the simulated logistics source datasets.
- `data_collection.py` – Loads and joins OMS, telemetry and warehouse data.
- `data_quality_audit.py` – Audits missing values, duplicates, invalid values and inconsistent labels.
- `clean_preprocess.py` – Performs the complete cleaning and preprocessing pipeline.
- `validate.py` – Performs final quality checks.
- `requirements.txt` – Required Python libraries.
- `data/` – Source and cleaned datasets.

## Data Quality Issues Covered

- Duplicate order records
- Missing delivery times
- Missing traffic telemetry
- Missing destination coordinates
- Inconsistent hub labels
- Inconsistent delivery-status labels
- Invalid distance values
- Negative/zero parcel weights
- Different feature scales

## Cleaning Techniques

1. Remove duplicate `order_id` records.
2. Standardize categorical labels.
3. Flag cancelled orders instead of imputing delivery time.
4. Impute `traffic_index` using hub/hour grouped medians.
5. Remove records without usable destination coordinates.
6. Detect distance outliers using the IQR method.
7. Remove non-physical parcel weights.
8. Apply Min-Max scaling to geographic clustering features.
9. Apply StandardScaler to regression features.
10. Validate the final dataset.

## Run the Pipeline

```bash
pip install -r requirements.txt

python generate_data.py
python data_collection.py
python data_quality_audit.py
python clean_preprocess.py
python validate.py
```

The final analysis-ready file is:

```text
data/orders_cleaned.csv
```
