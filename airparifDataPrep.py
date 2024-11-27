# Module by Hugo BONNELL

import pandas as pd

def getAirparifData(filePath: str):
    '''
    Gets all the csv files of the directory given and treats them to build usable datasets\n
    To work, the datasets must be those intended !\n
    Gives a df for hourly data and for daily data.
    '''

    df2018 = pd.read_csv(filePath+"/PA18_2018.csv")
    df2019 = pd.read_csv(filePath+"/PA18_2019.csv")
    df2020 = pd.read_csv(filePath+"/PA18_2020.csv")
    df2021 = pd.read_csv(filePath+"/PA18_2021.csv")
    df2022 = pd.read_csv(filePath+"/PA18_2022.csv")
    df2023 = pd.read_csv(filePath+"/PA18_2023.csv")
    df2024 = pd.read_csv(filePath+"/PA18_2024.csv")

    dataFrames = [df2018, df2019, df2020, df2021, df2022, df2023, df2024]

    # Rename the first column of all DataFrames in the list
    for i in range(len(dataFrames)):
        df = dataFrames[i]
        df.rename(columns={df.columns[0]: "date"}, inplace=True)            # Rename the first column
        df.columns = df.columns.str.replace(r'^PA18:', '', regex=True)      # Truncate column names by removing 'PA18:'
        dataFrames[i] = df.iloc[5:].reset_index(drop=True)                  # Remove rows 0 to 4

    
    combined_df = pd.concat(dataFrames, ignore_index=True)                  # Combine all dataframes in the list into one big dataframe    
    combined_df['date'] = pd.to_datetime(combined_df['date'])               # Convert the 'date' column to datetime
    
    hourly_df = combined_df                                                 # Save the hourly dataframe to return it later

    combined_df['date_only'] = combined_df['date'].dt.date                  # Extract the date (without the time part) from the 'date' column

    # Convert all columns (except 'date_only') to numeric, forcing errors to NaN
    combined_df[combined_df.columns.difference(['date', 'date_only'])] = combined_df[combined_df.columns.difference(['date', 'date_only'])].apply(pd.to_numeric, errors='coerce')

    daily_avg_df = combined_df.groupby('date_only').mean()                  # Group by the 'date_only' column and calculate the mean for each group    
    daily_avg_df.reset_index(inplace=True)                                  # Reset index to get 'date_only' as a regular column
    daily_avg_df.drop(columns=['date'], inplace=True)                       # Drop the 'date' column from daily_avg_df
    daily_avg_df.rename(columns={'date_only': 'date'}, inplace=True)        # Rename 'date_only' to 'date'

    return hourly_df, daily_avg_df