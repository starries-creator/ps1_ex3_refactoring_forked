# Pandas to Polars Cookbook

This repository adapts examples from [`pandas_cookbook`](https://github.com/jvns/pandas-cookbook) to teach common data analysis tasks with [Polars](https://pola.rs/). Chapters 1–3 and 5 retain Pandas examples for comparison; Chapter 4 uses a Polars data-processing flow.

Chapters 1–5 include Polars implementations. Chapters 6–8 retain the original Pandas examples and are starter examples for further Polars work.

## Set up

You need Git and Conda (Miniconda, Anaconda or Miniforge). From a terminal, clone this repository and create the project environment:

```bash
git clone https://github.com/starries-creator/ps1_ex3_refactoring_forked.git
cd ps1_ex3_refactoring_forked
conda env create -f environment.yml
conda activate polars_cookbook
```

Optionally open the repository in VS Code and select the `polars_cookbook` environment as the Python interpreter. The scripts in Chapters 1–5 resolve their bundled data files relative to each script, so the commands below work from the repository root.

## Run the chapters

Run a chapter from the activated environment:

```bash
python "cookbook/Chapter 1 - Reading from a CSV.py"
python "cookbook/Chapter 2 - Selecting data & findin the most common complain type.py"
python "cookbook/Chapter 3 - Which borough has the most noise complaints (or, more selecting data).py"
python "cookbook/Chapter 4 - Find out on which weekday people bike the most.py"
python "cookbook/Chapter 5 - Combining dataframes and scraping Canadian weather data.py"
```

The scripts display Matplotlib figures. Close each figure window to let execution continue. Chapter 5 needs an internet connection to download 12 monthly CSV files from the Government of Canada's weather service: 8,784 hourly observations for Montreal in 2012. As part of that exercise, it writes the combined result to `data/weather_2012.csv`, replacing the bundled file.

For a headless run (for example, in CI), set Matplotlib's backend to `Agg`:

```bash
MPLBACKEND=Agg python "cookbook/Chapter 1 - Reading from a CSV.py"
```

Replace the script path with the chapter you want to run.

## Assignment outline

The exercise is to adapt Pandas implementations to Polars, using Matplotlib or another suitable approach where direct Polars plotting is unavailable. Divide chapter ownership among the team so each member is responsible for at least one chapter. Make focused pull requests and review one another's changes.

For an introduction to Polars, see the [Calmcode Polars course](https://calmcode.io/course/polars/introduction).
