from data.sources.market_data import MarketData
from visualization.line_plot import LinePlot
from api.user_interface import Figure
from bokeh.models import ColumnDataSource

# Initialize Data Sources
aapl_data = MarketData(
    stock_name='AAPL',
    datetime_range=(
        '2024-05-01 09:30:00-04:00',
        '2024-05-01 09:40:00-04:00'
    ),
    columns=['price']
)
aapl_data.load_data()
aapl_data.downsample(rule='1s')

googl_data = MarketData(
    stock_name='GOOGL',
    datetime_range=(
        '2024-05-01 09:30:00-04:00',
        '2024-05-01 09:40:00-04:00'
    ),
    columns=['price']
)
googl_data.load_data()
googl_data.downsample(rule='1s')

# Create Plot
plot = LinePlot(title='Stock Prices Comparison', x_axis_label='Time', y_axis_label='Price (AAPL)')

# Compute the Dask DataFrames and create ColumnDataSources
aapl_source = ColumnDataSource(aapl_data.data.compute())
googl_source = ColumnDataSource(googl_data.data.compute())

# Add multiple lines to the plot with separate y-axes
plot.add_line(aapl_source, x_axis='timestamp', y_axis='price', color='blue', legend_label='AAPL')
plot.add_line(googl_source, x_axis='timestamp', y_axis='price', color='red', legend_label='GOOGL', y_range_name='googl')

# Configure the legend
plot.plot.legend.location = "top_left"

# Display Figure
fig = Figure()
fig.add_plot(plot)
fig.show()
