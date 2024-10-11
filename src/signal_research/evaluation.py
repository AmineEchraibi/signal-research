import numpy as np



def trailing_stop_return(df, idx, stop_loss_ratio=0.10):
    current_close = df.loc[idx, 'close']
    trailing_stop = current_close * (1 - stop_loss_ratio)
    max_price = current_close
    for i in range(idx + 1, len(df)):
        futur_close = df.loc[i, 'close']
        max_price = max(max_price, futur_close)
        trailing_stop = max(trailing_stop, max_price * (1 - stop_loss_ratio))
        return_ = (futur_close - current_close) / current_close
        if futur_close <= trailing_stop:
            return return_
        
        
        
        
        


def calculate_returns(df, monthly=True):
    if monthly:
    # Initialize columns for returns after each signal
        df['1_month_return'] = np.nan
        df['3_month_return'] = np.nan
        df['6_month_return'] = np.nan
        df['9_month_return'] = np.nan
        df['1_year_return'] = np.nan
        df['5_year_return'] = np.nan

        # Filter rows where there is a signal (either +1 or -1)
        signal_indices = df.index[df['signal'] != 0].tolist()

        for idx in signal_indices:
            current_close = df.loc[idx, 'close']

            # Calculate returns at each future time horizon
            if idx + 21 < len(df):  # 1-month return
                df.at[idx, '1_month_return'] = (df.loc[idx + 21, 'close'] - current_close) / current_close
            if idx + 63 < len(df):  # 3-month return
                df.at[idx, '3_month_return'] = (df.loc[idx + 63, 'close'] - current_close) / current_close
            if idx + 126 < len(df):  # 6-month return
                df.at[idx, '6_month_return'] = (df.loc[idx + 126, 'close'] - current_close) / current_close
            if idx + 189 < len(df):  # 9-month return
                df.at[idx, '9_month_return'] = (df.loc[idx + 189, 'close'] - current_close) / current_close
            if idx + 252 < len(df):  # 1-year return
                df.at[idx, '1_year_return'] = (df.loc[idx + 252, 'close'] - current_close) / current_close
            if idx + 1260 < len(df):  # 5-year return
                df.at[idx, '5_year_return'] = (df.loc[idx + 1260, 'close'] - current_close) / current_close

        return df
    df['return'] = np.nan
    signal_indices = df.index[df['signal'] != 0].tolist()
    for idx in signal_indices:
        df.at[idx,'return'] = trailing_stop_return(df, idx)
    return df

