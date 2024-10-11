import pandas as pd



def generateWeeklyBars(chart):
    weekly_chart = pd.DataFrame()
    chart["date"] = pd.to_datetime(chart["date"])
    chart = chart.set_index("date")
    weekly_chart["open"] = chart["open"].resample("W").first()
    weekly_chart["high"] = chart["high"].resample("W").max()
    weekly_chart["low"] = chart["low"].resample("W").min()
    weekly_chart["close"] = chart["close"].resample("W").last()
    weekly_chart["volume"] = chart["volume"].resample("W").sum()
    return weekly_chart.reset_index()