# PriceViz

PriceViz is a Python library designed for the processing, visualization, and analysis of large-scale time series data, with a particular focus on financial market data. It has two key offerings: parallelized downsampling of massive datasets so that they can fit into memory, and then visualization (or any sort of analysis) of key features (within and across tickers) in a flexible format.

## Installation

```bash
git clone https://github.com/dlevy233/TimeSeriesViz.git
cd TimeSeriesViz
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
pip install -e .
```

## Usage

Take a look at `example.py` for an illustration of the `PriceViz` module's usage. In brief, we can generate three large datasets (Parquet files) using `python generate_data.py --small` from within the `data` directory. The combined size of the three datasets (AAPL_data.parquet, GOOG_data.parquet, and NFLX_data.parquet, located in `data/small`) is 17.66 GB.

This data is far too large to instantiate a dataframe in memory for it. But we can do this (running `python example.py` from within `src`):

```python
df = load_dataset(
            sources=sources,
            granularity=timedelta(seconds=10),
            downsampling_strategy =
                DownsamplingStrategy(strategy="average_pooling"),
            name="example_dataset",
            datetime_column="timestamp"
        )
```

This use of the `load_dataset` function (which is the core of the `PriceViz` module) allows us to compose multiple time series datasets into one dataset while downsampling it in a highly parallelized fashion. The downsampling method is configurable. After the downsampling, the combined dataset is just 53.56 KB--ready for vizualization. Downsampled dataframes are cached.

You define the lines that you'd like to draw. Each line represents some property of a ticker, and can occuply one of a few different positions: OVERLAY, BELOW, and SIDE. BELOW shares an aligned x-axis with OVERLAY, and SIDE shares an aligned y-axis with OVERLAY.

```python
lines = [
LineSpec(ticker="AAPL", column="price", position=PlotPosition.OVERLAY),
LineSpec(ticker="NFLX", column="price", position=PlotPosition.OVERLAY),
LineSpec(ticker="GOOG", column="price", position=PlotPosition.OVERLAY),
LineSpec(ticker="AAPL", column="volume", position=PlotPosition.BELOW),
LineSpec(ticker="NFLX", column="volume", position=PlotPosition.BELOW),
LineSpec(ticker="GOOG", column="volume", position=PlotPosition.BELOW),
LineSpec(ticker="AAPL", column="price", position=PlotPosition.SIDE),
]

chart = plot_chart(
    df=df,
    lines=lines,
    chart_type="line",
    title="Stock Data: Multiple Tickers",
    output_filename="line_chart.html",
)
```
And then you can display the result with `open line_chart.html` from the CLI.

## Future improvements

- Increase the usage of lazy evaluation. Right now lazy evaluation is just used for downsampling until the dataframe is small enough to load into memory, but we can keep the data in a lazy state while we're plotting it or doing any sort of analysis. To do this, we would construct a set of supported transactions (which can be composed) and implement a lazy transaction execution engine (thankfully, frameworks like Dask make this relatively easy). A functional style for the API would be ideal for this.
- Improve the customizability and visual appeal of the plots, add more plot types, and support more output format options (e.g. send to some remote database).
- Improve the caching logic, using [cachey](https://github.com/dask/cachey) as inspiration (i.e. take both computation time and storage space into account, as well as frequency and recency of usage). And we can use the cloud for larger-scale caching.
- Support GPUs for greater parallelism, both for the data processing and data analysis (e.g. ML model training) tasks.
- Support parallelizing across multiple servers.
- Implement a far more abstract and flexible data model, supporting seamless usage of PriceViz across different types of data sources (e.g. SQL databases, NoSQL databases, Parquet files, etc.) with some kind of schema specification.
- Improve DevEx by adding an interactive option. This allows a user to "dive into" using the module without much mental overhead, and then during runtime the module will ask the user how they would like to handle things like unaligned x-axes, unbalanced data, etc.
