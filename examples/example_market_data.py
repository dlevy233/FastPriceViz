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
    msft_source = create_market_data('MSFT', start_time, end_time)
    amzn_source = create_market_data('AMZN', start_time, end_time)

    # Create Figure
    fig = Figure()

    # Example 1: Overlapped plots
    plot1 = LinePlot(title='AAPL and GOOGL (Overlapped)', x_axis_label='Time', y_axis_label='Price')
    plot1.add_line(aapl_source, x_axis='timestamp', y_axis='price', color='blue', legend_label='AAPL')
    plot1.add_line(googl_source, x_axis='timestamp', y_axis='price', color='red', legend_label='GOOGL', y_range_name='googl')
    fig.add_plot(plot1, position='overlap')

    # Example 2: Plot below
    plot2 = LinePlot(title='MSFT (Below)', x_axis_label='Time', y_axis_label='Price')
    plot2.add_line(msft_source, x_axis='timestamp', y_axis='price', color='green', legend_label='MSFT')
    fig.add_plot(plot2, position='below')

    # Example 3: Plot to the side
    plot3 = LinePlot(title='AMZN (Side)', x_axis_label='Time', y_axis_label='Price')
    plot3.add_line(amzn_source, x_axis='timestamp', y_axis='price', color='orange', legend_label='AMZN')
    fig.add_plot(plot3, position='side')

    # Display Figure
    fig.show()

if __name__ == "__main__":
    main()
