import dask.dataframe as dd

def load_data(path, columns=None):
    return dd.read_parquet(path, columns=columns)
