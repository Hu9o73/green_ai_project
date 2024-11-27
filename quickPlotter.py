# Module by Hugo BONNELL

import pandas as pd
import matplotlib.pyplot as plt

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