import logging
from datetime import timedelta
from typing import List
from priceviz import load_dataset
from priceviz.types import TimeSeriesSource, DataSourceType, DownsamplingStrategy
from priceviz.types import PlotPosition, LineSpec
from priceviz.plot_chart import plot_chart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_source(ticker: str) -> TimeSeriesSource:
    return TimeSeriesSource(
        filename=f"../data/small/{ticker}_data.parquet",
        source_type=DataSourceType.MARKET_DATA,
        ticker=ticker
    )

if __name__ == "__main__":
    try:
        # Create sources for each stock
        tickers = ["AAPL", "NFLX", "GOOG"]
        sources: List[TimeSeriesSource] = list(map(create_source, tickers))

        # Define parameters for load_dataset
        granularity = timedelta(seconds=10)
        downsampling_strategy = DownsamplingStrategy(strategy="average_pooling")
        dataset_name = "example_dataset"

        # Load the dataset
        df = load_dataset(
            sources=sources,
            granularity=granularity,
            downsampling_strategy=downsampling_strategy,
            name=dataset_name,
            datetime_column="timestamp"
        )

        # Check if the dataset was loaded successfully
        if df is None:
            logger.critical("Failed to load the dataset.")
            exit(1)

        # Define the lines to be plotted using LineSpec
        lines = [
            LineSpec(ticker="AAPL", column="price", position=PlotPosition.OVERLAY),
            LineSpec(ticker="NFLX", column="price", position=PlotPosition.OVERLAY),
            LineSpec(ticker="GOOG", column="price", position=PlotPosition.OVERLAY),
            LineSpec(ticker="AAPL", column="volume", position=PlotPosition.BELOW),
            LineSpec(ticker="NFLX", column="volume", position=PlotPosition.BELOW),
            LineSpec(ticker="GOOG", column="volume", position=PlotPosition.BELOW),
            LineSpec(ticker="AAPL", column="price", position=PlotPosition.SIDE),
        ]

        # Create the line chart with specified lines
        try:
            chart = plot_chart(
                df=df,
                lines=lines,
                chart_type="line",
                title="Stock Data: Multiple Tickers",
                output_filename="line_chart.html",
            )

            logger.info("Line chart created successfully.")
        except Exception as e:
            logger.error(f"Error creating line chart: {str(e)}")

    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
