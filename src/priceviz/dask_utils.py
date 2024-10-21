import os
from typing import Dict, Any
from dask.distributed import Client, LocalCluster
from dask import config as dask_config
from contextlib import contextmanager

def get_dask_config() -> Dict[str, Any]:
    """
    Get Dask configuration from environment variables or use default values.
    """
    return {
        'num_workers': int(os.environ.get('DASK_NUM_WORKERS', 4)),
        'threads_per_worker': int(os.environ.get('DASK_THREADS_PER_WORKER', 2)),
        'memory_limit': os.environ.get('DASK_MEMORY_LIMIT', '4GB'),
        'memory_target_fraction': float(os.environ.get('DASK_MEMORY_TARGET_FRACTION', 0.6)),
        'memory_spill_fraction': float(os.environ.get('DASK_MEMORY_SPILL_FRACTION', 0.7)),
        'memory_pause_fraction': float(os.environ.get('DASK_MEMORY_PAUSE_FRACTION', 0.8)),
        'memory_terminate_fraction': float(os.environ.get('DASK_MEMORY_TERMINATE_FRACTION', 0.95)),
    }

@contextmanager
def setup_dask_client(n_workers=4, threads_per_worker=2, memory_limit='2GB'):
    dask_config.set({
        'distributed.comm.timeouts.connect': '60s',
        'distributed.comm.timeouts.tcp': '60s',
        'distributed.comm.retry.count': 5,
        'distributed.worker.memory.target': 0.6,  # Target 60% memory use
        'distributed.worker.memory.spill': 0.7,   # Spill at 70% memory use
        'distributed.worker.memory.pause': 0.8,   # Pause worker at 80% use
        'distributed.worker.memory.terminate': 0.95,  # Restart worker at 95% use
    })
    
    cluster = LocalCluster(
        n_workers=n_workers,
        threads_per_worker=threads_per_worker,
        memory_limit=memory_limit,
        timeout=120
    )
    client = Client(cluster)
    try:
        yield client
    finally:
        client.close()
        cluster.close()
