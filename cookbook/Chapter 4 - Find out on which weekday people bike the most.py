# %%
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
import polars as pl

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
plt.rcParams["font.family"] = "sans-serif"

pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 60)

# %% Load the data
# TODO: Load the data using Polars
bikes = pl.read_csv(
    "data/bikes.csv",  
    separator=";",
    encoding="latin1",
    try_parse_dates=True
)

bikes.select(["Date", "Berri 1"]).to_pandas().plot(x="Date", y="Berri 1")
plt.show()

# %% Plot Berri 1 data
# TODO: Create a dataframe with just the Berri bikepath using Polars
pl_berri_bikes = bikes.select(["Date", "Berri 1"])

# %% Add weekday column
# TODO: Add a weekday column using Polars.
# Hint: Polars does not use an index.
pl_berri_bikes = pl_berri_bikes.with_columns(
    (pl.col("Date").dt.weekday() - 1).alias("weekday")
)

# %%
# TODO: Group by weekday and sum using Polars
weekday_counts = pl_berri_bikes.group_by("weekday").agg(
    pl.col("Berri 1").sum()
).sort("weekday")

# %% Rename index
# TODO: Rename index using Polars, if possible.
week_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_counts = weekday_counts.with_columns(
    pl.col("weekday").replace_strict({i: week_names[i] for i in range(7)}).alias("weekday_name")
)

# %% Plot results
# TODO: Plot results using Polars and matplotlib
weekday_counts.to_pandas().plot(kind="bar", x="weekday_name", y="Berri 1", legend=False)
plt.title("Cyclists by Weekday on Berri 1")
plt.xlabel("Weekday")
plt.ylabel("Number of Cyclists")
plt.show()

# %% Final message
print("Analysis complete!")