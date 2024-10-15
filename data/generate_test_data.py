import pandas as pd
import numpy as np
import os

# Generate the data
start_timestamp = pd.Timestamp('2024-05-01 09:30:00-0400', tz='America/New_York')
end_timestamp = pd.Timestamp('2024-05-01 09:40:00-0400', tz='America/New_York')

datetime_index = pd.date_range(start=start_timestamp, end=end_timestamp, freq='10U')
np.random.seed(42)
price_changes = np.random.normal(0, 0.00001, len(datetime_index))
price_changes = pd.Series(price_changes, index=datetime_index)

price_multipliers = 1 + price_changes
cumulative_product = price_multipliers.cumprod()

starting_price = 100
price_series = starting_price * cumulative_product

# Create DataFrame with 'timestamp' as a column
df = pd.DataFrame({'timestamp': datetime_index, 'price': price_series.values})

# Ensure data is sorted by 'timestamp'
df = df.sort_values('timestamp')

# Save to Parquet without the index
os.makedirs('data/market/AAPL/', exist_ok=True)
df.to_parquet('data/market/AAPL/sample.parquet', index=False)
