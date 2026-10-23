# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
URL_TEMPLATE = (
    "https://climate.meteo.gc.ca/climate_data/bulk_data_e.html"
    "?format=csv&stationID=5415&Year={year}&Month={month}"
    "&Day=1&timeframe=1&submit=Download+Data"
)


@lru_cache(maxsize=12)
def download_weather_csv(year, month):
    # Reuse each official UTF-8 CSV for the Pandas and Polars examples.
    with urlopen(URL_TEMPLATE.format(year=year, month=month), timeout=30) as response:
        return response.read()

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 3)
plt.rcParams["font.family"] = "sans-serif"

# %%
# By the end of this chapter, we'll have downloaded the Montreal station's hourly weather data for 2012 and saved it to a CSV. We'll download one month at a time, then combine the months.
# Here's the temperature every hour for 2012!

weather_2012_final = pd.read_csv(
    DATA_DIR / "weather_2012.csv", index_col="date_time", parse_dates=True
)
weather_2012_final["temperature_c"].plot(figsize=(15, 6))
plt.show()

# TODO: rewrite using Polars

weather_2012_final_pl = pl.read_csv(
    DATA_DIR / "weather_2012.csv",
    try_parse_dates=True
)

plt.figure(figsize=(15, 6))
plt.plot(
    weather_2012_final_pl["date_time"].to_list(),
    weather_2012_final_pl["temperature_c"].to_list()
)
plt.show()

# %%
# Okay, let's start from the beginning.
# We're going to get the data for March 2012, and clean it up
# The original cookbook's URL no longer works. Use the current official HTTPS
# endpoint above; both libraries read the same downloaded UTF-8 CSV bytes.

year = 2012
month = 3
url_march = URL_TEMPLATE.format(month=month, year=year)
weather_mar2012 = pd.read_csv(
    BytesIO(download_weather_csv(year, month)),
    index_col="Date/Time (LST)",
    parse_dates=True,
    encoding="utf-8-sig",
    header=0,
)
weather_mar2012.head()

# TODO: rewrite using Polars. Yes, Polars can handle URLs similarly.

weather_mar2012_pl = pl.read_csv(
    download_weather_csv(year, month),
    try_parse_dates=True,
    infer_schema_length=None,
    null_values=["", "NA", "NaN", "N/A"],
)

weather_mar2012_pl.head()

# %%
# Let's clean up the data a bit.
# You'll notice in the summary above that there are a few columns which are are either entirely empty or only have a few values in them. Let's get rid of all of those with `dropna`.
# The argument `axis=1` to `dropna` means "drop columns", not rows", and `how='any'` means "drop the column if any value is null".
weather_mar2012 = weather_mar2012.dropna(axis=1, how="any")
weather_mar2012[:5]

# This is much better now -- we only have columns with real data.

# TODO: rewrite using Polars

weather_mar2012_pl = weather_mar2012_pl.select([
    col for col in weather_mar2012_pl.columns
    if weather_mar2012_pl[col].null_count() == 0
])

weather_mar2012_pl[:5]


# %%
# Let's get rid of columns that we do not need.
# For example, the year, month, day, time columns are redundant (we have Date/Time (LST) column).
# Let's get rid of those. The `axis=1` argument means "Drop columns", like before. The default for operations like `dropna` and `drop` is always to operate on rows.
weather_mar2012 = weather_mar2012.drop(["Year", "Month", "Day", "Time (LST)"], axis=1)
weather_mar2012[:5]

# TODO: redo this using polars

weather_mar2012_pl = weather_mar2012_pl.drop(["Year", "Month", "Day", "Time (LST)"])
weather_mar2012_pl[:5]

# %%
# When you look at the data frame, you see that some column names have some weird characters in them.
# Let's clean this up, too.
# Let's print the column names first:
weather_mar2012.columns

# And now rename the columns to make it easier to work with
weather_mar2012.columns = weather_mar2012.columns.str.replace(
    'ï»¿"', ""
)  # Remove the weird characters at the beginning
weather_mar2012.columns = weather_mar2012.columns.str.replace(
    "Â", ""
)  # Remove the weird characters at the

# TODO: rewrite using Polars

weather_mar2012_pl = weather_mar2012_pl.rename({
    col: col.replace('ï»¿"', "").replace("Â", "")
    for col in weather_mar2012_pl.columns
})


# %%
# Optionally, you can also rename columns more manually for specific cases:
weather_mar2012 = weather_mar2012.rename(
    columns={
        "Longitude (x)": "Longitude",
        "Latitude (y)": "Latitude",
        "Station Name": "Station_Name",
        "Climate ID": "Climate_ID",
        "Temp (°C)": "Temperature_C",
        "Dew Point Temp (°C)": "Dew_Point_Temp_C",
        "Rel Hum (%)": "Relative_Humidity",
        "Wind Spd (km/h)": "Wind_Speed_kmh",
        "Visibility (km)": "Visibility_km",
        "Stn Press (kPa)": "Station_Pressure_kPa",
        "Weather": "Weather",
    }
)
weather_mar2012.index.name = "date_time"

# Check the new column names
print(weather_mar2012.columns)

# Some people also prefer lower case column names.
weather_mar2012.columns = weather_mar2012.columns.str.lower()
print(weather_mar2012.columns)

# TODO: redo this using polars

column_mapping = {
    "Longitude (x)": "Longitude",
    "Latitude (y)": "Latitude",
    "Station Name": "Station_Name",
    "Climate ID": "Climate_ID",
    "Temp (°C)": "Temperature_C",
    "Dew Point Temp (°C)": "Dew_Point_Temp_C",
    "Rel Hum (%)": "Relative_Humidity",
    "Wind Spd (km/h)": "Wind_Speed_kmh",
    "Visibility (km)": "Visibility_km",
    "Stn Press (kPa)": "Station_Pressure_kPa",
    "Weather": "Weather",
    "Date/Time (LST)": "date_time"
}

weather_mar2012_pl = weather_mar2012_pl.rename({
    old: new for old, new in column_mapping.items()
    if old in weather_mar2012_pl.columns
})

print(weather_mar2012_pl.columns)

weather_mar2012_pl = weather_mar2012_pl.rename({
    col: col.lower()
    for col in weather_mar2012_pl.columns
}).select("date_time", pl.exclude("date_time"))

print(weather_mar2012_pl.columns)

# %%
# Notice how it goes up to 25° C in the middle there? That was a big deal. It was March, and people were wearing shorts outside.
plt.figure()
weather_mar2012["temperature_c"].plot(figsize=(15, 5))
plt.show()

# TODO: redo this using polars

plt.figure(figsize=(15, 5))
plt.plot(
    weather_mar2012_pl["date_time"].to_list(),
    weather_mar2012_pl["temperature_c"].to_list()
)
plt.show()

# %%
# This one's just for fun -- we've already done this before, using groupby and aggregate! We will learn whether or not it gets colder at night. Well, obviously. But let's do it anyway.
temperatures = weather_mar2012[["temperature_c"]].copy()
print(temperatures.head())
temperatures.loc[:, "Hour"] = weather_mar2012.index.hour
temperatures.groupby("Hour").aggregate(np.median).plot()
plt.show()

# So it looks like the time with the highest median temperature is 2pm. Neat.

# TODO: redo this using polars

temperatures_pl = weather_mar2012_pl.select(
    ["temperature_c"]
).with_columns(
    weather_mar2012_pl["date_time"].dt.hour().alias("Hour")
)

print(temperatures_pl.head())

hourly_median_pl = temperatures_pl.group_by("Hour").agg(
    pl.col("temperature_c").median()
).sort("Hour")

plt.figure()
plt.plot(
    hourly_median_pl["Hour"].to_list(),
    hourly_median_pl["temperature_c"].to_list()
)
plt.show()

# %%
# Okay, so what if we want the data for the whole year? Ideally the API would just let us download that, but I couldn't figure out a way to do that.
# First, let's put our work from above into a function that gets the weather for a given month.


def clean_data(data):
    data = data.dropna(axis=1, how="any")
    data = data.drop(["Year", "Month", "Day", "Time (LST)"], axis=1)
    data.columns = data.columns.str.replace('ï»¿"', "")
    data.columns = data.columns.str.replace("Â", "")
    data = data.rename(
        columns={
            "Longitude (x)": "Longitude",
            "Latitude (y)": "Latitude",
            "Station Name": "Station_Name",
            "Climate ID": "Climate_ID",
            "Temp (°C)": "Temperature_C",
            "Dew Point Temp (°C)": "Dew_Point_Temp_C",
            "Rel Hum (%)": "Relative_Humidity",
            "Wind Spd (km/h)": "Wind_Speed_kmh",
            "Visibility (km)": "Visibility_km",
            "Stn Press (kPa)": "Station_Pressure_kPa",
            "Weather": "Weather",
        }
    )
    data.columns = data.columns.str.lower()
    data.index.name = "date_time"
    return data


def download_weather_month(year, month):
    weather_data = pd.read_csv(
        BytesIO(download_weather_csv(year, month)),
        index_col="Date/Time (LST)",
        parse_dates=True,
        encoding="utf-8-sig",
    )
    weather_data_clean = clean_data(weather_data)
    return weather_data_clean


# TODO: redefine these functions using polars and your code above

def clean_data_pl(data):
    data = data.select([
        col for col in data.columns
        if data[col].null_count() == 0
    ])

    data = data.drop(
        ["Year", "Month", "Day", "Time (LST)"]
    )

    data = data.rename({
        col: col.replace('ï»¿"', "").replace("Â", "")
        for col in data.columns
    })

    column_mapping = {
        "Longitude (x)": "Longitude",
        "Latitude (y)": "Latitude",
        "Station Name": "Station_Name",
        "Climate ID": "Climate_ID",
        "Temp (°C)": "Temperature_C",
        "Dew Point Temp (°C)": "Dew_Point_Temp_C",
        "Rel Hum (%)": "Relative_Humidity",
        "Wind Spd (km/h)": "Wind_Speed_kmh",
        "Visibility (km)": "Visibility_km",
        "Stn Press (kPa)": "Station_Pressure_kPa",
        "Weather": "Weather",
        "Date/Time (LST)": "date_time"
    }

    data = data.rename({
        old: new for old, new in column_mapping.items()
        if old in data.columns
    })

    data = data.rename({
        col: col.lower()
        for col in data.columns
    }).select("date_time", pl.exclude("date_time"))

    return data


def download_weather_month_pl(year, month):
    weather_data = pl.read_csv(
        download_weather_csv(year, month),
        try_parse_dates=True,
        infer_schema_length=None,
        null_values=["", "NA", "NaN", "N/A"],
    )

    weather_data_clean = clean_data_pl(weather_data)

    return weather_data_clean

# %%
download_weather_month(2012, 1)[:5]
# %%
# Now, let's use a list comprehension to download all our data and then just concatenate these data frames
# This might take a while
data_by_month = [download_weather_month(2012, i) for i in range(1, 13)]
weather_2012 = pd.concat(data_by_month)
weather_2012.head()

# TODO: do the same with polars

data_by_month_pl = [
    download_weather_month_pl(2012, i)
    for i in range(1, 13)
]

weather_2012_pl = pl.concat(
    data_by_month_pl,
    how="diagonal_relaxed"
)

weather_2012_pl.head()

# %%
# Now, let's save the data.
weather_2012.to_csv(DATA_DIR / "weather_2012.csv")

# TODO: use polars to save the data.

weather_2012_pl.write_csv(
    DATA_DIR / "weather_2012.csv", datetime_format="%Y-%m-%d %H:%M:%S"
)
