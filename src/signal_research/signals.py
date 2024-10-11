

def generate_regression_signal(df, indicator_name):
    # Initialize the signal column
    df['signal'] = 0

    # Check if the close price has crossed above the upper confidence band
    condition_upper = (df[indicator_name] > df['regression_upper']) & \
                      (df[indicator_name].shift(1) <= df['regression_upper'].shift(1)) & \
                      (df[indicator_name] > df[indicator_name].shift(1)) & \
                      (df[indicator_name].shift(1) > df[indicator_name].shift(2)) & \
                      (df[indicator_name].shift(2) > df[indicator_name].shift(3))

    # Check if the close price has crossed below the lower confidence band
    condition_lower = (df[indicator_name] < df['regression_lower']) & \
                      (df[indicator_name].shift(1) >= df['regression_lower'].shift(1)) & \
                      (df[indicator_name] < df[indicator_name].shift(1)) & \
                      (df[indicator_name].shift(1) < df[indicator_name].shift(2)) & \
                      (df[indicator_name].shift(2) < df[indicator_name].shift(3))

    # Assign +1 to the signal column where the upper condition is met
    df.loc[condition_upper, 'signal'] = 1

    # Assign -1 to the signal column where the lower condition is met
    df.loc[condition_lower, 'signal'] = -1

    return df

