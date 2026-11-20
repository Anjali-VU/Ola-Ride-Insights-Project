import pandas as pd
import numpy as np

# Load raw OLA bookings data
df = pd.read_csv("OLA_DataSet.xlsx - July.csv")

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

# Convert date and time fields
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time

# Create analysis-friendly date features
df["Booking_Date"] = df["Date"].dt.date
df["Booking_Hour"] = pd.to_datetime(
    df["Time"].astype(str), format="%H:%M:%S", errors="coerce"
).dt.hour
df["Booking_Day"] = df["Date"].dt.day_name()
df["Booking_Month"] = df["Date"].dt.month_name()
df["Booking_Day_Number"] = df["Date"].dt.dayofweek

# Trim whitespace from text columns
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].map(lambda value: value.strip() if isinstance(value, str) else value)

# IMPORTANT:
# Do not impute ratings, payment methods, cancellation reasons, or time metrics
# blindly. Missing values may be structurally missing for unsuccessful bookings.

df.to_csv("OLA_Cleaned.csv", index=False)
print("Cleaning complete. Saved OLA_Cleaned.csv")
print("Rows:", len(df), "| Columns:", len(df.columns))
print("Duplicates remaining:", df.duplicated().sum())
