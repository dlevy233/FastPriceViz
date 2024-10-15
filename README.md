# TimeSeriesViz

A Python library for efficient visualization of high-frequency time series data.

## Features

- **Flexible API**: Customize visualizations for various data sources
- **Distributed Computing**: Use Dask to handle large datasets efficiently
- **Interactive Plots**: Create dynamic visualizations with Bokeh
- **Downsampling**: Optimize performance with efficient data reduction
- **Timezone Support**: Proper handling of timezone-aware datetime data

## Installation

### Clone the Repository

bash
Copy code
git clone https://github.com/dlevy233/TimeSeriesViz.git
cd TimeSeriesViz
### Create and Activate a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
### Install Dependencies and the Package

bash
Copy code
pip install -r requirements.txt
pip install -e .

## Usage

1. Generate Test Data: Run `python data/generate_test_data.py` to create sample data.
2. Visualize Data: Use the API to load, downsample, and plot time series data.

## Project Structure

- `data/`: Data generation and source classes
  - `generate_test_data.py`: Script to create sample data
  - `sources/`: Data source implementations
- `compute/`: Distributed computing utilities (Dask)
- `visualization/`: Plotting classes and visualization components
- `api/`: User-facing API for composing visualizations
- `utils/`: Helper functions and utilities
- `tests/`: Unit and integration tests
- `examples/`: Example scripts demonstrating usage
