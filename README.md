# TimeSeriesViz

A Python library for efficient visualization of high-frequency time series data.

## Features

- **Flexible API**: Customize visualizations for various data sources
- **Distributed Computing**: Use Dask to handle large datasets efficiently
- **Interactive Plots**: Create dynamic visualizations with Bokeh
- **Downsampling**: Optimize performance with efficient data reduction
- **Timezone Support**: Proper handling of timezone-aware datetime data

## Installation

* Clone the Repository
* Create and Activate a Virtual Environment
* Install Dependencies and the Package

    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```

## Usage

1. Generate Test Data: Run `python data/generate_test_data.py` to create sample data.
2. Run Example: Execute `python examples/example_market_data.py` to see a sample visualization of stock price data.

## API Design and Usage

The TimeSeriesViz API is designed to be flexible and easy to use. Here's an overview of the main components:

### Data Sources

- `MarketData`: Loads and processes market data from Parquet files.
  ```python
  data = MarketData(stock_name='AAPL', datetime_range=(start_time, end_time), columns=['price'])
  data.load_data()
  data.downsample(rule='1s')
  ```

### Visualization

- `LinePlot`: Creates line plots for time series data.
  ```python
  plot = LinePlot(title='Stock Prices', x_axis_label='Time', y_axis_label='Price')
  plot.add_line(source, x_axis='timestamp', y_axis='price', color='blue', legend_label='AAPL')
  ```

### Figure Composition

- `Figure`: Combines multiple plots into a single figure.
  ```python
  fig = Figure()
  fig.add_plot(plot1, position='overlap')
  fig.add_plot(plot2, position='below')
  fig.add_plot(plot3, position='side')
  fig.show()
  ```

### Layout Options

The `Figure` class supports three layout options:
- `'overlap'`: Plots are overlaid on the same axes
- `'below'`: Plots are stacked vertically
- `'side'`: Plots are placed side by side

### Example

## Project Structure

- `data/`: Data generation and source classes
  - `generate_test_data.py`: Script to create sample data
  - `sources/`: Data source implementations
- `compute/`: Distributed computing utilities (Dask)
- `visualization/`: Plotting classes and visualization components
- `api/`: User-facing API for composing visualizations
- `utils/`: Helper functions and utilities
- `tests/`: Unit and integration tests
- `examples/`: Example scripts demonstrating usage
