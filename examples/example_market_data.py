from data.sources.market_data import MarketData
from visualization.line_plot import LinePlot
from api.user_interface import Figure
import pandas as pd

# Initialize Data Source
market_data = MarketData(
    stock_name='AAPL',
    datetime_range=(
        '2024-05-01 09:30:00-04:00',
        '2024-05-01 09:40:00-04:00'
    ),
    columns=['price']
)
market_data.load_data()
market_data.downsample(rule='1s')

# Create Plot with data_source
plot = LinePlot(title='AAPL Stock Price', data_source=market_data)

# Display Figure
fig = Figure()
fig.add_plot(plot)
fig.show()
