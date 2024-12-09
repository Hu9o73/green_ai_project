# Module by Hugo BONNELL

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def quickPlot(df : pd.DataFrame, timeCol: str, y: str, movingAverage = False, movingAverageWindow = 7): 
    '''
    Prints a given y column's value according to time.\n
    Can handle printing the moving average if specified.\n
    Returns a plt object that can later be modifed (adding title etc...)
    '''

    # Convert the time column 'timeCol' to datetime format
    df[timeCol] = pd.to_datetime(df[timeCol])
    
    #Plot data
    plt.figure(figsize=(10, 6))

    if (movingAverage):
        df['moving_avg'] = df[y].rolling(window=movingAverageWindow).mean()
        plt.plot(df[timeCol], df['moving_avg'])
    else:
        plt.plot(df[timeCol], df[y])

    plt.xlabel("Date", fontsize=14)
    plt.ylabel(y, fontsize=14)

    return plt


def quickRegPlot(df : pd.DataFrame, timeCol: str, y: str, movingAverage=False, movingAverageWindow=7): 
    '''
    Prints a given y column's value according to time.\n
    Can handle printing the moving average if specified.\n
    Adds a linear regression line if desired.\n
    Returns a plt object that can later be modified (adding title etc...).
    '''
    dfNoNa = df[[timeCol, y]].dropna()
    # Convert the time column 'timeCol' to datetime format
    dfNoNa[timeCol] = pd.to_datetime(dfNoNa[timeCol])
    
    # Ensure the 'timeCol' is in numeric format for regression
    dfNoNa['time_numeric'] = pd.to_numeric(dfNoNa[timeCol])

    # Plot data
    plt.figure(figsize=(10, 6))

    if movingAverage:
        dfNoNa['moving_avg'] = dfNoNa[y].rolling(window=movingAverageWindow).mean()
        plt.plot(dfNoNa[timeCol], dfNoNa['moving_avg'], label=f'{y} (Moving Avg)', color='b')
    else:
        plt.plot(dfNoNa[timeCol], dfNoNa[y], label=f'{y}', color='b')

    # Add linear regression dashed line
    X = dfNoNa['time_numeric'].values.reshape(-1, 1)  # Convert to 2D array
    y_values = dfNoNa[y].values  # Dependent variable
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y_values)
    
    # Predict values based on the linear regression model
    y_pred = model.predict(X)
    
    # Plot the linear regression line
    plt.plot(dfNoNa[timeCol], y_pred, label='Linear Regression', linestyle='--', color='r')

    # Add labels and title
    plt.xlabel("Date", fontsize=14)
    plt.ylabel(y, fontsize=14)
    plt.legend()

    return plt


def avgPollutantLevelPerHour(pollutant: str, hourly_df: pd.DataFrame):
    hourly_df['hour'] = hourly_df['date'].dt.hour
    average_per_hour = hourly_df.groupby('hour')[pollutant].mean()
    
    average_per_hour_df = average_per_hour.reset_index()
    average_per_hour_df.columns = ['Hour', f'Average {pollutant} Level']

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(average_per_hour_df['Hour'], average_per_hour_df[f'Average {pollutant} Level'], marker='o', linestyle='-')
    plt.title(f'Average {pollutant} Levels Per Hour (All Dates)', fontsize=16)
    plt.xlabel('Hour of the Day', fontsize=14)
    plt.ylabel(f'{pollutant} Concentration', fontsize=14)
    plt.xticks(range(0, 24), fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.show()


def avgAllPolutantsPerHour(hourly_df: pd.DataFrame):
    pollutants = ["PM10", "NO2", "NO", "NOX", "O3"]
    hourly_df['hour'] = hourly_df['date'].dt.hour
    plt.figure(figsize=(10,6))
    # Calculate hourly averages for each pollutant and plot them
    for pollutant in pollutants:
        if pollutant in hourly_df.columns:  # Ensure the pollutant exists in the data
            hourly_avg = hourly_df.groupby('hour')[pollutant].mean()
            plt.plot(hourly_avg.index, hourly_avg.values, marker='o', label=pollutant)

    # Add title, labels, and legend
    plt.title(f'Average Levels of Pollutants', fontsize=16)
    plt.xlabel('Hour of the Day', fontsize=14)
    plt.ylabel('Concentration', fontsize=14)
    plt.xticks(range(0, 24), fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()


def pollutantLevelsOnDay(specific_day: str, pollutant: str, hourly_df: pd.DataFrame):
    # Filter the data for the specific day
    specific_day = pd.to_datetime(specific_day)
    filtered_df = hourly_df[hourly_df['date'].dt.date == specific_day.date()]

    # Plot the data for the specific day
    if not filtered_df.empty:
        plot = quickPlot(filtered_df, "date", pollutant)
        plot.title(f"{pollutant} levels on {specific_day}")
        plt.show()
    else:
        print(f"No data available for {specific_day}.")


def avgAllPolutantsPerMonth(daily_df: pd.DataFrame):
    pollutants = ["PM10", "NO2", "NO", "NOX", "O3"]
    
    # Ensure the 'date' column is in datetime format
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    # Extract the month from the datetime
    daily_df['month'] = daily_df['date'].dt.month

    # Initialize a plot
    plt.figure(figsize=(10, 6))

    # Calculate monthly averages for each pollutant and plot them
    for pollutant in pollutants:
        if pollutant in daily_df.columns:  # Ensure the pollutant exists in the data
            monthly_avg = daily_df.groupby('month')[pollutant].mean()
            plt.plot(monthly_avg.index, monthly_avg.values, marker='o', label=pollutant)

    # Add title, labels, and legend
    plt.title('Average Levels of Pollutants Grouped by Month', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Concentration', fontsize=14)
    plt.xticks(range(1, 13), [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], fontsize=10, rotation=45)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()


def avgAllPolutantsPerYear(daily_df: pd.DataFrame):
    pollutants = ["PM10", "NO2", "NO", "NOX", "O3"]
    
    # Ensure the 'date' column is in datetime format
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    # Extract the month from the datetime
    daily_df['year'] = daily_df['date'].dt.year

    # Initialize a plot
    plt.figure(figsize=(10, 6))

    # Calculate monthly averages for each pollutant and plot them
    for pollutant in pollutants:
        if pollutant in daily_df.columns:  # Ensure the pollutant exists in the data
            monthly_avg = daily_df.groupby('year')[pollutant].mean()
            plt.plot(monthly_avg.index, monthly_avg.values, marker='o', label=pollutant)

    # Add title, labels, and legend
    plt.title('Average Levels of Pollutants Grouped by Year', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Concentration', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()


