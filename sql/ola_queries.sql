-- OLA Ride Insights | MySQL 8+ | Table: ola_bookings
-- Q1: Retrieve all successful bookings
SELECT * FROM ola_bookings WHERE Booking_Status = 'Success';

-- Q2: Average ride distance for each vehicle type
SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS avg_ride_distance
FROM ola_bookings GROUP BY Vehicle_Type ORDER BY avg_ride_distance DESC;

-- Q3: Number of rides cancelled by customers
SELECT COUNT(*) AS customer_cancelled_rides
FROM ola_bookings WHERE Booking_Status = 'Canceled by Customer';

-- Q4: Top 5 customers by number of bookings
SELECT Customer_ID, COUNT(*) AS ride_count
FROM ola_bookings GROUP BY Customer_ID ORDER BY ride_count DESC LIMIT 5;

-- Q5: Driver cancellations due to personal/car-related issues
SELECT COUNT(*) AS driver_personal_car_cancellations
FROM ola_bookings
WHERE Booking_Status = 'Canceled by Driver'
  AND Canceled_Rides_by_Driver LIKE '%Personal & Car related issue%';

-- Q6: Maximum and minimum driver ratings for Prime Sedan bookings
SELECT MAX(Driver_Ratings) AS max_driver_rating,
       MIN(Driver_Ratings) AS min_driver_rating
FROM ola_bookings WHERE Vehicle_Type = 'Prime Sedan';

-- Q7: All rides paid using UPI
SELECT * FROM ola_bookings WHERE Payment_Method = 'UPI';

-- Q8: Average customer rating per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating
FROM ola_bookings GROUP BY Vehicle_Type ORDER BY avg_customer_rating DESC;

-- Q9: Total booking value for successful rides
SELECT ROUND(SUM(Booking_Value), 2) AS successful_booking_value
FROM ola_bookings WHERE Booking_Status = 'Success';

-- Q10: Incomplete rides and their reasons
SELECT Booking_ID, Customer_ID, Vehicle_Type, Booking_Date, Booking_Hour,
       Incomplete_Rides, Incomplete_Rides_Reason
FROM ola_bookings
WHERE Incomplete_Rides = 'Yes' OR Booking_Status LIKE '%Incomplete%';
