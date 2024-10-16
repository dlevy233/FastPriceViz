import pandas as pd
import numpy as np
import os

def generate_price_data(start_price, seed):
    start_timestamp = pd.Timestamp('2024-05-01 09:30:00.000-0400', tz='America/New_York')
    end_timestamp = pd.Timestamp('2024-05-01 09:40:00.000-0400', tz='America/New_York')

    datetime_index = pd.date_range(start=start_timestamp, end=end_timestamp, freq='1ms')
    np.random.seed(seed)
    price_changes = np.random.normal(0, 0.00001, len(datetime_index))
    price_changes = pd.Series(price_changes, index=datetime_index)

    price_multipliers = 1 + price_changes
    cumulative_product = price_multipliers.cumprod()

    price_series = start_price * cumulative_product

    # Create DataFrame with 'timestamp' as a column
    df = pd.DataFrame({'timestamp': datetime_index, 'price': price_series.values})

    # Ensure data is sorted by 'timestamp'
    df = df.sort_values('timestamp')
    
    return df

# Generate data for AAPL
aapl_df = generate_price_data(start_price=100, seed=42)

# Generate data for GOOGL
googl_df = generate_price_data(start_price=2500, seed=43)

# Generate data for MSFT
msft_df = generate_price_data(start_price=300, seed=44)

# Generate data for AMZN
amzn_df = generate_price_data(start_price=3300, seed=45)

# Save AAPL data to Parquet
os.makedirs('data/market/AAPL/', exist_ok=True)
aapl_df.to_parquet('data/market/AAPL/sample.parquet', index=False)

# Save GOOGL data to Parquet
os.makedirs('data/market/GOOGL/', exist_ok=True)
googl_df.to_parquet('data/market/GOOGL/sample.parquet', index=False)

# Save MSFT data to Parquet
os.makedirs('data/market/MSFT/', exist_ok=True)
msft_df.to_parquet('data/market/MSFT/sample.parquet', index=False)

# Save AMZN data to Parquet
os.makedirs('data/market/AMZN/', exist_ok=True)
amzn_df.to_parquet('data/market/AMZN/sample.parquet', index=False)
