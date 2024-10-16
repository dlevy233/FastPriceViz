# TimeSeriesViz

A Python library for efficient visualization of high-frequency time series data, designed to handle large-scale financial market data with millisecond precision.

## Features

- **High-Frequency Data Support**: Handle time series data with granularity down to 1 millisecond.
- **Large-Scale Data Processing**: Efficiently manage datasets up to 100 million rows and 1000 columns.
- **Flexible API**: Customize visualizations for various data sources and layouts.
- **Distributed Computing**: Utilize Dask for efficient handling of large datasets.
- **Interactive Plots**: Create dynamic visualizations with Bokeh.
- **Adaptive Downsampling**: Optimize performance with efficient data reduction based on zoom levels.
- **Timezone Support**: Proper handling of timezone-aware datetime data.
- **Caching System**: Keep recently accessed time ranges in memory for faster repeated access.
- **Multiple Plot Layouts**: Support for overlapped, stacked, and side-by-side plot arrangements.

## Installation

1. Clone the Repository:
   ```
   git clone https://github.com/yourusername/TimeSeriesViz.git
   cd TimeSeriesViz
   ```

2. Create and Activate a Virtual Environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install Dependencies and the Package:
   ```
   pip install -r requirements.txt
   pip install -e .
   ```

## Usage

1. Generate Test Data:
   ```
   python data/generate_test_data.py
   ```
   This creates sample data for AAPL, GOOGL, MSFT, and AMZN stocks with millisecond precision.

2. Run Example:
   ```
   python examples/example_market_data.py
   ```
   This demonstrates various visualization capabilities, including different plot layouts and resolutions.

## API Design and Usage

### Data Sources

- `MarketData`: Loads and processes market data from Parquet files, with caching for improved performance.
  ```python
  data = MarketData(stock_name='AAPL', datetime_range=(start_time, end_time), columns=['price'])
  df = data.get_data(resolution='100ms')  # Get data at 100ms resolution
  ```

### Visualization

- `LinePlot`: Creates line plots for time series data.
  ```python
  plot = LinePlot(title='Stock Prices', x_axis_label='Time', y_axis_label='Price')
  plot.add_line(source, x_axis='timestamp', y_axis='price', color='blue', legend_label='AAPL')
  ```

### Figure Composition

- `Figure`: Combines multiple plots into a single figure with various layout options.
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

### Caching and Performance

- Manage the cache size:
  ```python
  MarketData.set_cache_size(10)  # Set cache to hold 10 items
  MarketData.clear_cache()  # Clear the entire cache
  ```

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

## Performance Considerations

- The library uses Dask for distributed computing, allowing it to handle large datasets efficiently.
- Adaptive downsampling is implemented to optimize performance at different zoom levels.
- Caching of recently accessed data ranges improves response times for repeated queries.
- When visualizing, it's acceptable to miss some data points (e.g., spikes) in favor of better performance, especially at higher zoom levels.

## Testing

To run the test suite, use the following command from the project root directory:
```
python -m unittest discover tests
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.
