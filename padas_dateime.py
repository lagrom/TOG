import pandas as pd
import datetime
import numpy as np

dti = pd.to_datetime(
    ["1/1/2018", np.datetime64("2018-01-01"), datetime.datetime(2018, 1, 1)])

dti

dti = pd.date_range("2018-01-01", periods=3, freq="H")
dti

dti = dti.tz_localize("UTC")
dti

dti.tz_convert("US/Pacific")
dti

idx = pd.date_range("2018-01-01", periods=5, freq="H")

ts = pd.Series(range(len(idx)), index=idx)

ts

ts.resample("2H").mean()

friday = pd.Timestamp("2018-01-05")
friday.day_name()

saturday = friday + pd.Timedelta("1 day")
saturday.day_name()

# Add 1 business day (Friday --> Monday)
monday = friday + pd.offsets.BDay()
monday.day_name()
