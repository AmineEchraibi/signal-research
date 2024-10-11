import numpy as np
import scipy.stats as stats


def add_average_true_range(df, period):
    # Ensure the dataframe is sorted by date
    
    # Calculate the True Range (TR)
    df['previous_close'] = df['close'].shift(1)
    df['high_low'] = df['high'] - df['low']
    df['high_prev_close'] = abs(df['high'] - df['previous_close'])
    df['low_prev_close'] = abs(df['low'] - df['previous_close'])
    
    df['true_range'] = df[['high_low', 'high_prev_close', 'low_prev_close']].max(axis=1)
    
    # Calculate the ATR using a rolling mean over the specified period
    df['ATR'] = df['true_range'].ewm(com=period, adjust=False).mean()
    
    # Drop temporary columns used for calculations
    df.drop(['previous_close', 'high_low', 'high_prev_close', 'low_prev_close', 'true_range'], axis=1, inplace=True)
    
    return df

def add_bollinger_bands(df, period=20, multiplier=2):
    # Calculate the moving average (MA)
    df['bollinger'] = df['close'].ewm(com=period, adjust=False).mean()
    
    # Calculate the standard deviation (SD)
    df['standard_deviation'] = df['close'].rolling(window=period, min_periods=1, closed='left').std()
    
    # Calculate the upper and lower Bollinger Bands
    df['bollinger_upper'] = df['bollinger'] + (df['standard_deviation'] * multiplier)
    df['bollinger_lower'] = df['bollinger'] - (df['standard_deviation'] * multiplier)
    
    return df


def add_donchian_channels(df, period=20):


    df['donchian_upper'] = df['high'].rolling(window=period, closed='left').max()
    df['donchian_lower'] = df['low'].rolling(window=period, closed='left').min()
    df['donchian'] = (df['donchian_upper'] + df['donchian_lower']) / 2
    return df
    



def VolumeAdjustedHighLowDelta(df, period):
    df['VolumeAdjustedHighLowDelta'] = np.log(df['volume'].ewm(com=period, adjust=False).mean() * (df['high'].ewm(com=period, adjust=False).mean() - df['low'].ewm(com=period, adjust=False).mean()) / df['close'].ewm(com=period, adjust=False).mean())
    return df


def add_rolling_regression(df, column, window=20, confidence=0.95):
    # Initialize columns for regression results
    df['regression'] = np.nan
    df['regression_upper'] = np.nan
    df['regression_lower'] = np.nan
    
    # Iterate through the DataFrame using a rolling window
    for i in range(window, len(df)):
        window_df = df.iloc[i-window:i]
        x = np.arange(len(window_df))
        y = window_df[column].values
        
        # Perform linear regression on the rolling window data
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Predicted values using the regression model
        y_pred = intercept + slope * x
        # Calculate standard error of the regression
        se = np.sqrt(np.sum((y - y_pred) ** 2) / (len(y) - 2))
        
        # t-score for the confidence interval
        t_score = stats.t.ppf((1 + confidence) / 2, df=len(y) - 2)
        
        # Confidence interval band calculation
        conf_interval = t_score * se * np.sqrt(1 / len(y) + (x - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
        
        # Assign fitted values and confidence bands to the main DataFrame
        df.at[i, 'regression'] = y_pred[-1]
        df.at[i, 'regression_upper'] = y_pred[-1] + conf_interval[-1]
        df.at[i, 'regression_lower'] = y_pred[-1] - conf_interval[-1]
    
    return df