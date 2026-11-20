# OLA Ride Insights

Ride-sharing analytics project using Python, SQL, Power BI, and Streamlit.

## Folder structure
- `data/OLA_Cleaned.csv`: cleaned dataset for the app and Power BI.
- `data/clean_data.py`: reusable cleaning script (expects the raw file in its working directory).
- `sql/ola_queries.sql`: 10 business queries for MySQL 8+.
- `power_bi/DAX_Measures.txt`: DAX measures and dashboard page plan.
- `app/app.py`: interactive Streamlit analytics application.

## Run the Streamlit application
1. Install Python 3.10+.
2. Open a terminal in this project folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `streamlit run app/app.py`

The app uses the included cleaned CSV and offers date, vehicle, booking status, and payment filters. It includes Overview, Vehicle Type, Revenue, Cancellation, Ratings, and Data Explorer sections.


## SQL setup (MySQL 8+)
Create a database, import `data/OLA_Cleaned.csv` into a table named `ola_bookings`, and ensure column names match the CSV exactly. Then execute queries in `sql/ola_queries.sql`.

Suggested table types: text columns VARCHAR; Date and Booking_Date DATE; Time VARCHAR or TIME; Booking_Hour and Booking_Day_Number INT; V_TAT and C_TAT DOUBLE; Booking_Value and Ride_Distance numeric; ratings DECIMAL(3,2). MySQL import wizard can infer types; review them before loading.

## Power BI
1. Get Data > Text/CSV > `data/OLA_Cleaned.csv`.
2. Verify data types: Booking_Date date, numeric metrics/rating fields numeric, IDs/text fields text.
3. Create the measures listed in `power_bi/DAX_Measures.txt`.
4. Build the five pages listed in the same guide: Overall, Vehicle Type, Revenue, Cancellation, Ratings.
5. Add slicers for date and vehicle/status/payment where applicable.

## Data notes
- Preserve missing values; blank ratings/payment fields can be structurally missing for unsuccessful rides.
- Do not treat all rows as successful rides when calculating successful booking value.
- The dashboard and app are descriptive analytics, not fraud-detection proof.

## Deliverables
Dataset, cleaning script, SQL file, Streamlit app, Power BI build guide and DAX measures. The Power BI `.pbix` itself must be created and saved from Power BI Desktop.
