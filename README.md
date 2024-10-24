# Naive Forecasting Analysis with Time Series Data

## Project Overview
This project focuses on creating and analyzing naive forecasts from a dataset containing point forecasts. Using Python libraries such as `pandas` and `numpy`, we will compute naive forecasting methods, evaluate their performance using error metrics, and visualize the results with boxplots and histograms.

## Task 1: Naive Forecasting Methods

### 1.1: Downloading the Dataset
- Download the dataset with 3 point forecasts (L02b List 5) from the ePortal under T02+L02 Time series graphics.
  
### 1.2: Loading the Data
- Load the dataset using either `numpy` or `pandas`.

### 1.3: Naive Forecast Preparation
- **Naive Forecast 1**: Prepare a new column that uses the last half-hourly real observation as the forecast for the next observation. Note that there will be no forecast for the first half-hourly observation.
- **Naive Forecast 2**: Create a new column that uses the value from the corresponding half-hourly period from the previous day as the forecast.
- **Naive Forecast 3**:
  - Use the value from the corresponding half-hourly observation of the previous day for days that are not holidays.
  - For holidays, use the value from the corresponding half-hourly observation of the last Sunday or the last holiday, whichever is closer to the forecasted date.

### 1.4: Error Metrics Calculation
- Compute the Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) for all three naive forecasts, specifically for all data points from the years 2013 and 2014.

### 1.5: Boxplot Preparation
- For each naive forecast, prepare a boxplot of the Mean Absolute Percentage Error (MAPE) of the daily averages for all data points from 2013 and 2014. 
- The boxplots should differentiate between holidays and non-holidays, presenting the results in three separate subplots arranged in a single figure (one row of three columns).

### 1.6: RMSE Calculation for Combined Forecasts
- Compute the RMSE scores of the half-hourly values for all three naive methods and the three forecasts from the file for the year 2013.
- Find the best equally weighted combination of the six forecasts by evaluating every possible combination (from 1 to 6 forecasts) and calculating the combined forecast (an equally weighted average).
- Plot a histogram of the RMSE values for all combined forecasts, including the total number of combinations in the title.

### 1.7: MAE Calculation for Best Combination
- For the best combination identified in point 1.6, compute its MAE for the month of your birthday in the year 2014.
- Print the result in the format: "The MAE of the best combination in {MONTH} 2014 is {RESULT}."

## Libraries Used
- **Pandas** for data manipulation and analysis.
- **Numpy** for numerical computations.
- **Matplotlib** for data visualization (boxplots and histograms).
