import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(page_title='OLA Ride Insights', page_icon='🚕', layout='wide')
DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'OLA_Cleaned.csv'
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Booking_Date'] = pd.to_datetime(df['Booking_Date'], errors='coerce')
    return df

df = load_data()
st.title('🚕 OLA Ride Insights')
st.caption('Ride-sharing and mobility analytics | Booking trends, revenue, vehicles, cancellations and ratings')

with st.sidebar:
    st.header('Filters')
    min_date, max_date = df['Booking_Date'].min().date(), df['Booking_Date'].max().date()
    date_range = st.date_input('Booking date range', value=(min_date, max_date), min_value=min_date, max_value=max_date)
    vehicles = st.multiselect('Vehicle type', sorted(df['Vehicle_Type'].dropna().unique()), default=list(sorted(df['Vehicle_Type'].dropna().unique())) )
    statuses = st.multiselect('Booking status', sorted(df['Booking_Status'].dropna().unique()), default=list(sorted(df['Booking_Status'].dropna().unique())) )
    payments = st.multiselect('Payment method', sorted(df['Payment_Method'].dropna().unique()), default=list(sorted(df['Payment_Method'].dropna().unique())) )
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = df[df['Booking_Date'].between(start, end)]
    else:
        filtered = df.copy()
    filtered = filtered[filtered['Vehicle_Type'].isin(vehicles) & filtered['Booking_Status'].isin(statuses)]
    # Payment filter preserves rows with missing payment values when all available methods are selected.
    if payments and len(payments) < df['Payment_Method'].dropna().nunique():
        filtered = filtered[filtered['Payment_Method'].isin(payments)]

success = filtered[filtered['Booking_Status'].eq('Success')]
customer_cancel = filtered[filtered['Booking_Status'].eq('Canceled by Customer')]
driver_cancel = filtered[filtered['Booking_Status'].eq('Canceled by Driver')]
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Bookings', f'{len(filtered):,}')
col2.metric('Successful rides', f'{len(success):,}')
col3.metric('Customer cancellations', f'{len(customer_cancel):,}')
col4.metric('Driver cancellations', f'{len(driver_cancel):,}')
col5.metric('Successful booking value', f'₹{success.Booking_Value.sum():,.0f}')

page = st.selectbox('Analysis section', ['Overall', 'Vehicle Type', 'Revenue', 'Cancellation', 'Ratings', 'Data Explorer'])
if page == 'Overall':
    a,b = st.columns(2)
    trend = filtered.groupby('Booking_Date', dropna=False).size().reset_index(name='Bookings')
    a.plotly_chart(px.line(trend, x='Booking_Date', y='Bookings', markers=True, title='Ride Volume Over Time'), use_container_width=True)
    status = filtered['Booking_Status'].value_counts().rename_axis('Status').reset_index(name='Bookings')
    b.plotly_chart(px.pie(status, names='Status', values='Bookings', hole=.45, title='Booking Status Breakdown'), use_container_width=True)
    st.subheader('Booking data overview')
    st.dataframe(filtered.head(1000), use_container_width=True)
elif page == 'Vehicle Type':
    v = filtered.groupby('Vehicle_Type').agg(Bookings=('Booking_ID','count'), Total_Distance=('Ride_Distance','sum'), Avg_Distance=('Ride_Distance','mean'), Successful_Value=('Booking_Value', lambda x: x[filtered.loc[x.index,'Booking_Status'].eq('Success')].sum()), Avg_Customer_Rating=('Customer_Rating','mean')).reset_index()
    a,b = st.columns(2)
    a.plotly_chart(px.bar(v.sort_values('Total_Distance', ascending=False).head(5), x='Vehicle_Type', y='Total_Distance', title='Top Vehicle Types by Ride Distance'), use_container_width=True)
    b.plotly_chart(px.bar(v, x='Vehicle_Type', y='Bookings', title='Bookings by Vehicle Type'), use_container_width=True)
    st.dataframe(v.round(2), use_container_width=True)
elif page == 'Revenue':
    a,b = st.columns(2)
    rev = filtered.groupby('Payment_Method', dropna=False)['Booking_Value'].sum().reset_index().dropna(subset=['Payment_Method'])
    a.plotly_chart(px.bar(rev, x='Payment_Method', y='Booking_Value', title='Booking Value by Payment Method'), use_container_width=True)
    top = success.groupby('Customer_ID')['Booking_Value'].sum().nlargest(5).reset_index()
    b.plotly_chart(px.bar(top, x='Customer_ID', y='Booking_Value', title='Top 5 Customers by Successful Booking Value'), use_container_width=True)
    daily = filtered.groupby('Booking_Date')['Ride_Distance'].sum().reset_index()
    st.plotly_chart(px.line(daily, x='Booking_Date', y='Ride_Distance', markers=True, title='Ride Distance by Day'), use_container_width=True)
elif page == 'Cancellation':
    a,b = st.columns(2)
    cr = customer_cancel['Canceled_Rides_by_Customer'].value_counts(dropna=True).reset_index()
    cr.columns=['Reason','Count']
    dr = driver_cancel['Canceled_Rides_by_Driver'].value_counts(dropna=True).reset_index()
    dr.columns=['Reason','Count']
    a.plotly_chart(px.bar(cr, x='Reason', y='Count', title='Customer Cancellation Reasons'), use_container_width=True)
    b.plotly_chart(px.bar(dr, x='Reason', y='Count', title='Driver Cancellation Reasons'), use_container_width=True)
    st.write('Incomplete rides')
    st.dataframe(filtered[filtered['Incomplete_Rides'].eq('Yes')][['Booking_ID','Vehicle_Type','Incomplete_Rides_Reason']], use_container_width=True)
elif page == 'Ratings':
    a,b = st.columns(2)
    a.plotly_chart(px.histogram(filtered.dropna(subset=['Driver_Ratings']), x='Driver_Ratings', nbins=10, title='Driver Ratings Distribution'), use_container_width=True)
    b.plotly_chart(px.histogram(filtered.dropna(subset=['Customer_Rating']), x='Customer_Rating', nbins=10, title='Customer Ratings Distribution'), use_container_width=True)
    rating = filtered.groupby('Vehicle_Type')[['Driver_Ratings','Customer_Rating']].mean().reset_index()
    st.plotly_chart(px.bar(rating, x='Vehicle_Type', y=['Driver_Ratings','Customer_Rating'], barmode='group', title='Average Ratings by Vehicle Type'), use_container_width=True)
else:
    st.subheader('Explore filtered data')
    st.write(f'{len(filtered):,} rows currently match your filters.')
    st.dataframe(filtered, use_container_width=True)
    st.download_button('Download filtered data as CSV', filtered.to_csv(index=False).encode('utf-8'), 'ola_filtered.csv', 'text/csv')

st.divider()
st.caption('OLA Ride Insights | Built with Python, Pandas, Streamlit and Plotly')
