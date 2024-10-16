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
   This demonstrates various visualization capabilities, including:
   - Overlapped plots (AAPL and GOOGL)
   - Plots below (MSFT)
   - Plots to the side (AMZN)
   - Zoomed-in view with adaptive resolution (AAPL 1-minute zoom)

## API Documentation

### Data Sources

#### DataSource (Base Class)

## Performance Considerations

## Handling Sources with Different Non-Aligned X-axes

When dealing with data sources that have different, non-aligned X-axes, consider the following approaches:

1. **Resampling**: Resample all data sources to a common time interval. This approach works well when the differences in time intervals are small or when some loss of precision is acceptable.

   ```python
   def align_sources(*sources, common_interval='1s'):
       aligned_sources = []
       for source in sources:
           aligned_sources.append(source.resample(common_interval).mean())
       return aligned_sources
   ```

2. **Interpolation**: For sources with different but close time points, use interpolation to estimate values at matching timestamps.

   ```python
   def interpolate_sources(*sources, method='linear'):
       # Combine all unique timestamps
       all_timestamps = sorted(set().union(*[source.index for source in sources]))
       interpolated_sources = []
       for source in sources:
           interpolated_sources.append(source.reindex(all_timestamps).interpolate(method=method))
       return interpolated_sources
   ```

3. **Flexible Plotting**: Implement plotting functions that can handle multiple X-axes, allowing each data source to maintain its original timestamps.

   ```python
   def plot_multi_axis(sources, labels):
       fig, ax1 = plt.subplots()
       for i, (source, label) in enumerate(zip(sources, labels)):
           if i == 0:
               ax = ax1
           else:
               ax = ax1.twinx()
           ax.plot(source.index, source.values, label=label)
           ax.set_ylabel(label)
       plt.title('Multi-Source Plot with Different X-axes')
       plt.legend()
       plt.show()
   ```

4. **Time Range Bucketing**: For vastly different time scales, consider bucketing the data into larger time ranges and comparing the aggregated statistics.

## Alternative API Designs for Improved Performance

To further enhance the performance of the system, consider the following API changes and design alternatives:

1. **Lazy Evaluation**: Implement a lazy evaluation system where operations on data are not performed until explicitly requested.

   ```python
   class LazyDataSource:
       def __init__(self, source):
           self.source = source
           self.operations = []

       def transform(self, operation):
           self.operations.append(operation)
           return self

       def compute(self):
           result = self.source
           for operation in self.operations:
               result = operation(result)
           return result
   ```

2. **Streaming API**: Design an API that supports streaming data processing, allowing for real-time updates and reducing memory usage.

   ```python
   class StreamingDataSource:
       def __init__(self, source_generator):
           self.source_generator = source_generator

       def process_stream(self, chunk_size=1000):
           for chunk in self.source_generator(chunk_size):
               yield self.process_chunk(chunk)

       def process_chunk(self, chunk):
           # Process the chunk of data
           return processed_chunk
   ```

3. **Distributed Processing**: Extend the API to support distributed processing across multiple nodes.

   ```python
   from dask.distributed import Client

   class DistributedDataSource:
       def __init__(self, sources):
           self.sources = sources
           self.client = Client()

       def process_distributed(self):
           futures = [self.client.submit(self.process_source, source) for source in self.sources]
           return self.client.gather(futures)

       def process_source(self, source):
           # Process individual source
           return processed_data
   ```

4. **Adaptive Resolution**: Implement an API that automatically adjusts the data resolution based on the viewing window or available computational resources.

   ```python
   class AdaptiveResolutionSource:
       def __init__(self, source):
           self.source = source

       def get_data(self, view_range, max_points=1000):
           data_range = self.source.get_data_range()
           if (view_range[1] - view_range[0]) / (data_range[1] - data_range[0]) < 0.1:
               return self.source.get_downsampled_data(view_range, max_points)
           else:
               return self.source.get_full_resolution_data(view_range)
   ```

5. **Precomputed Aggregations**: Design an API that supports precomputed aggregations at various time scales to speed up common queries.

   ```python
   class PrecomputedAggregationSource:
       def __init__(self, source):
           self.source = source
           self.aggregations = {
               '1h': self.precompute_aggregation('1h'),
               '1d': self.precompute_aggregation('1d'),
               '1w': self.precompute_aggregation('1w')
           }

       def precompute_aggregation(self, interval):
           # Precompute and store aggregations
           pass

       def get_data(self, interval):
           if interval in self.aggregations:
               return self.aggregations[interval]
           else:
               return self.source.get_data().resample(interval).mean()
   ```

These alternative API designs and approaches can significantly improve the performance and flexibility of the TimeSeriesViz library, allowing it to handle even larger datasets and more complex visualization scenarios.


## Testing

The TimeSeriesViz library includes a comprehensive test suite to ensure the reliability and correctness of its components. The tests cover various aspects of the library, including data sources, computation, visualization, and user interface.

### Running Tests

To run the entire test suite, use the following command from the project root directory:

```
python -m unittest discover tests
```

### Test Structure

The test suite is organized into several files, each focusing on a specific component of the library:

1. `test_data_sources.py`: Tests for the data source classes, including `MarketData`.
2. `test_compute.py`: Tests for the distributed computing functionality using Dask.
3. `test_visualization.py`: Tests for the visualization components, particularly the `LinePlot` class.
4. `test_user_interface.py`: Tests for the `Figure` class and its layout capabilities.