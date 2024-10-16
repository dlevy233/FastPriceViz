from data.sources.market_data import MarketData
from visualization.line_plot import LinePlot
from api.user_interface import Figure
from bokeh.models import ColumnDataSource
import pandas as pd

def create_market_data(stock_name, start_time, end_time, view_range=None):
    data = MarketData(
        stock_name=stock_name,
        datetime_range=(start_time, end_time),
        columns=['price']
    )
    return ColumnDataSource(data.get_data(view_range=view_range).compute())

def main():
    start_time = '2024-05-01 09:30:00-04:00'
    end_time = '2024-05-01 09:40:00-04:00'

    # Create Figure
    fig = Figure()

    # Example 1: Overlapped plots
    plot1 = LinePlot(title='AAPL and GOOGL (Overlapped)', x_axis_label='Time', y_axis_label='Price')
    aapl_source = create_market_data('AAPL', start_time, end_time)
    googl_source = create_market_data('GOOGL', start_time, end_time)
    plot1.add_line(aapl_source, x_axis='timestamp', y_axis='price', color='blue', legend_label='AAPL')
    plot1.add_line(googl_source, x_axis='timestamp', y_axis='price', color='red', legend_label='GOOGL', y_range_name='googl')
    fig.add_plot(plot1, position='overlap')

    # Example 2: Plot below
    plot2 = LinePlot(title='MSFT (Below)', x_axis_label='Time', y_axis_label='Price')
    msft_source = create_market_data('MSFT', start_time, end_time)
    plot2.add_line(msft_source, x_axis='timestamp', y_axis='price', color='green', legend_label='MSFT')
    fig.add_plot(plot2, position='below')

    # Example 3: Plot to the side
    plot3 = LinePlot(title='AMZN (Side)', x_axis_label='Time', y_axis_label='Price')
    amzn_source = create_market_data('AMZN', start_time, end_time)
    plot3.add_line(amzn_source, x_axis='timestamp', y_axis='price', color='orange', legend_label='AMZN')
    fig.add_plot(plot3, position='side')

    # Example 4: Zoomed-in view (1 minute)
    zoom_start = pd.Timestamp('2024-05-01 09:35:00-04:00')
    zoom_end = pd.Timestamp('2024-05-01 09:36:00-04:00')
    plot4 = LinePlot(title='AAPL (1 Minute Zoom)', x_axis_label='Time', y_axis_label='Price')
    aapl_zoomed = create_market_data('AAPL', start_time, end_time, view_range=(zoom_start, zoom_end))
    plot4.add_line(aapl_zoomed, x_axis='timestamp', y_axis='price', color='purple', legend_label='AAPL (Zoomed)')
    fig.add_plot(plot4, position='below')

    # Display Figure
    fig.show()

if __name__ == "__main__":
    main()
