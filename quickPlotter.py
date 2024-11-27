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
    plt.figure(figsize=(12, 8))

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
    dfNoNa = df.dropna()
    # Convert the time column 'timeCol' to datetime format
    dfNoNa[timeCol] = pd.to_datetime(dfNoNa[timeCol])
    
    # Ensure the 'timeCol' is in numeric format for regression
    dfNoNa['time_numeric'] = pd.to_numeric(dfNoNa[timeCol])

    # Plot data
    plt.figure(figsize=(12, 8))

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