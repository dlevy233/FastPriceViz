import psutil

def suggest_resources():
    num_cores = psutil.cpu_count(logical=False)
    return {
        'num_workers': num_cores,
        'num_partitions': num_cores
    }
