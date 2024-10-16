from data.sources.market_data import MarketData
from visualization.line_plot import LinePlot
from api.user_interface import Figure
from bokeh.models import ColumnDataSource

def create_market_data(stock_name, start_time, end_time):
    data = MarketData(
        stock_name=stock_name,
        datetime_range=(start_time, end_time),
        columns=['price']
    )
    data.load_data()
    data.downsample(rule='1s')
    return ColumnDataSource(data.data.compute())

def main():
    # Initialize Data Sources
    start_time = '2024-05-01 09:30:00-04:00'
    end_time = '2024-05-01 09:40:00-04:00'

    aapl_source = create_market_data('AAPL', start_time, end_time)
    googl_source = create_market_data('GOOGL', start_time, end_time)

    # Create Plot
    plot = LinePlot(title='Stock Prices Comparison', x_axis_label='Time', y_axis_label='Price')

    # Add multiple lines to the plot with separate y-axes
    plot.add_line(aapl_source, x_axis='timestamp', y_axis='price', color='blue', legend_label='AAPL')
    plot.add_line(googl_source, x_axis='timestamp', y_axis='price', color='red', legend_label='GOOGL', y_range_name='googl')

    # Display Figure
    fig = Figure()
    fig.add_plot(plot)
    fig.show()

if __name__ == "__main__":
    main()
