import dask.dataframe as dd
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import argparse
from tqdm import tqdm
import signal
import logging
import time
import functools
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Global flag for cancellation
cancel_flag = False

def signal_handler(sig, frame):
    global cancel_flag
    print("\nCancellation requested. Finishing current chunk and exiting...")
    cancel_flag = True

# Retry decorator with exponential backoff
def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise
                    sleep = (backoff_in_seconds * 2 ** x +
                             random.uniform(0, 1))
                    time.sleep(sleep)
                    x += 1
                    logger.warning(f"Retrying {func.__name__}. Attempt {x} of {retries}")
        return wrapper
    return decorator

def generate_stock_data_chunk(symbol, start_timestamp, end_timestamp, starting_price, volatility):
    datetime_index = pd.date_range(start=start_timestamp, end=end_timestamp, freq='10us')
    price_changes = np.random.normal(0, volatility, len(datetime_index))
    price_multipliers = 1 + price_changes
    cumulative_product = np.cumprod(price_multipliers)
    price_series = starting_price * cumulative_product
    
    volume = np.random.poisson(1000, len(datetime_index))
    bid = price_series - np.random.uniform(0, 0.02, len(datetime_index))
    ask = price_series + np.random.uniform(0, 0.02, len(datetime_index))
    
    df = dd.from_pandas(pd.DataFrame({
        'timestamp': datetime_index,
        'price': price_series,
        'volume': volume,
        'bid': bid,
        'ask': ask
    }), npartitions=1)
    
    return df

@retry_with_backoff(retries=3, backoff_in_seconds=1)
def save_to_parquet(df, filepath, partition):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    partition_path = f"{filepath}/part.{partition}.parquet"
    
    try:
        if not os.path.exists(filepath):
            logger.debug(f"Writing new file: {partition_path}")
            df.to_parquet(partition_path, engine='pyarrow', compression='snappy')
        else:
            logger.debug(f"Appending to file: {partition_path}")
            df.to_parquet(partition_path, engine='pyarrow', compression='snappy', append=True, ignore_divisions=True)
    except Exception as e:
        logger.error(f"Error saving data to {partition_path}: {e}")
        raise

def generate_stock_parquet(symbol, starting_price, volatility, start_timestamp, end_timestamp, output_dir, chunk_size):
    global cancel_flag
    filepath = os.path.join(SCRIPT_DIR, output_dir, f'{symbol}_data.parquet')
    
    chunk_start = start_timestamp
    partition = 0
    
    total_chunks = int((end_timestamp - start_timestamp) / pd.Timedelta(minutes=chunk_size)) + 1
    
    with tqdm(total=total_chunks, 
              desc=f"Generating {symbol} data", 
              unit="chunk",
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} chunks [{elapsed}<{remaining}, {rate_fmt}{postfix}]") as pbar:
        while chunk_start < end_timestamp and not cancel_flag:
            chunk_end = min(chunk_start + pd.Timedelta(minutes=chunk_size), end_timestamp)
            df_chunk = generate_stock_data_chunk(symbol, chunk_start, chunk_end, starting_price, volatility)
            
            try:
                save_to_parquet(df_chunk, filepath, partition)
                partition += 1
            except Exception as e:
                logger.error(f"Failed to save data for {symbol}: {e}")
                return False
            
            chunk_start = chunk_end + pd.Timedelta(microseconds=10)
            pbar.set_postfix({"current_time": chunk_start.strftime("%Y-%m-%d %H:%M:%S")})
            pbar.update(1)
    
    return True

def generate_all_stocks(small=True, big=True, chunk_size=1):
    stocks = [
        ('AAPL', 150, 0.00001),
        ('NFLX', 400, 0.000015),
        ('GOOG', 2500, 0.000012)
    ]
    
    tasks = []
    
    if small:
        start_small = pd.Timestamp('2024-05-01 09:30:00-0400', tz='America/New_York')
        end_small = pd.Timestamp('2024-05-01 10:00:00-0400', tz='America/New_York')
        tasks.extend([(stock, start_small, end_small, 'small') for stock in stocks])
    
    if big:
        start_big = pd.Timestamp('2024-05-01 09:30:00-0400', tz='America/New_York')
        end_big = pd.Timestamp('2024-05-01 16:00:00-0400', tz='America/New_York')
        tasks.extend([(stock, start_big, end_big, 'big') for stock in stocks])
    
    with ProcessPoolExecutor() as executor:
        futures = []
        for stock, start, end, output_dir in tasks:
            futures.append(executor.submit(generate_stock_parquet, *stock, start, end, output_dir, chunk_size))
        
        for future in as_completed(futures):
            if cancel_flag:
                executor.shutdown(wait=False)
                break
            if not future.result():
                print(f"Failed to generate data for a stock")

    if small and not cancel_flag:
        print_file_info(os.path.join(SCRIPT_DIR, 'small', 'AAPL_data.parquet'), 'small')
    if big and not cancel_flag:
        print_file_info(os.path.join(SCRIPT_DIR, 'big', 'AAPL_data.parquet'), 'big')

def print_file_info(filepath, size):
    try:
        df = dd.read_parquet(filepath)
        num_rows = df.shape[0].compute()
        num_cols = len(df.columns)
        time_range = dd.compute(df['timestamp'].min(), df['timestamp'].max())
        
        print(f"Generated {size} Parquet dataset contains:")
        print(f"Number of rows: {num_rows:,}")
        print(f"Number of columns: {num_cols}")
        print(f"Time range: {time_range[0]} to {time_range[1]}")
        print()
    except FileNotFoundError:
        print(f"Parquet dataset not found: {filepath}")
    except Exception as e:
        print(f"Error reading Parquet dataset {filepath}: {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate stock data Parquet files")
    parser.add_argument("--small", action="store_true", help="Generate small dataset")
    parser.add_argument("--big", action="store_true", help="Generate big dataset")
    parser.add_argument("--chunk-size", type=int, default=1, help="Chunk size in minutes for data generation")
    args = parser.parse_args()

    if not (args.small or args.big):
        print("Please specify at least one of --small or --big")
    else:
        # Set up signal handler for graceful cancellation
        signal.signal(signal.SIGINT, signal_handler)
        
        generate_all_stocks(small=args.small, big=args.big, chunk_size=args.chunk_size)
        
        if cancel_flag:
            print("Operation cancelled. Partial data may have been generated.")
        else:
            print("Parquet files generated successfully.")
