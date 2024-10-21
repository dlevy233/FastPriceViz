from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, Range1d
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import gridplot
import pandas as pd
import logging
from typing import List, Literal, Dict
from priceviz.types import PlotPosition, LineSpec

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a list of colors to use for different lines
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def plot_chart(
    df: pd.DataFrame,
    lines: List[LineSpec],
    chart_type: Literal["line", "bar"] = "line",
    title: str = "Stock Data",
    output_filename: str = "chart.html",
):
    try:
        # Log DataFrame info
        logger.info(f"DataFrame columns: {df.columns.tolist()}")
        logger.info(f"DataFrame info:\n{df.info()}")
        logger.info(f"DataFrame head:\n{df.head()}")

        if chart_type == "line":
            plots = plot_line_chart(df, lines, title)
        elif chart_type == "bar":
            plots = plot_bar_chart(df, lines, title)
        else:
            raise ValueError("Invalid chart type. Expected 'line' or 'bar'.")
        
        layout = create_layout(plots)
        save_plot(layout, output_filename)
        logger.info(f"Chart plotted successfully and saved as {output_filename}")
        return layout
    except Exception as e:
        logger.error(f"Error in plotting chart: {str(e)}", exc_info=True)
        raise

def plot_line_chart(df: pd.DataFrame, lines: List[LineSpec], title: str):
    logger.info(f"Plotting line chart with {len(lines)} lines")

    plots = {pos: create_bokeh_figure(f"{title} - {pos.value.capitalize()}") for pos in PlotPosition}

    # Determine if we're using a DatetimeIndex or a timestamp column
    if isinstance(df.index, pd.DatetimeIndex):
        timestamp_column = df.index.name or 'timestamp'
        df = df.reset_index()
    else:
        timestamp_column = next((col for col in df.columns if 'time' in col.lower()), None)
        if timestamp_column is None:
            raise ValueError("No timestamp column found in the DataFrame")

    x_range = Range1d(start=df[timestamp_column].min(), end=df[timestamp_column].max())

    for i, line in enumerate(lines):
        ticker_data = df[df['ticker'] == line.ticker] if 'ticker' in df.columns else df
        if line.column in ticker_data.columns:
            p = plots[line.position]
            color = line.color or COLORS[i % len(COLORS)]
            p = create_line_plot(p, ticker_data, color, line.ticker, line.column, timestamp_column)
        else:
            logger.warning(f"Column '{line.column}' not found for ticker '{line.ticker}'")

    # Set x_range for all plots
    for p in plots.values():
        p.x_range = x_range

    return {pos: p for pos, p in plots.items() if len(p.renderers) > 0}

def create_line_plot(p, data, color, ticker, column, timestamp_column):
    source_data = data[[timestamp_column, column]].copy()
    source_data['ticker'] = ticker
    source_data['value'] = source_data[column]
    source = ColumnDataSource(source_data)
    
    p.line(x=timestamp_column, y=column, source=source, color=color, line_width=2, 
           legend_label=f"{ticker} - {column}")
    p.legend.click_policy = "hide"
    return p

def plot_bar_chart(df: pd.DataFrame, lines: List[LineSpec], title: str):
    # Implement bar chart plotting logic here
    # This is a placeholder and should be implemented based on your specific requirements
    logger.warning("Bar chart plotting is not implemented yet")
    return {PlotPosition.OVERLAY: create_bokeh_figure(title)}

def create_bokeh_figure(title: str, width: int = 800, height: int = 300) -> figure:
    p = figure(title=title, x_axis_type="datetime", width=width, height=height)
    
    p.xaxis.formatter = DatetimeTickFormatter(
        hours="%d %B %Y %H:%M:%S",
        days="%d %B %Y %H:%M:%S",
        months="%d %B %Y %H:%M:%S",
        years="%d %B %Y %H:%M:%S"
    )
    p.xaxis.major_label_orientation = 0.7

    hover = HoverTool(
        tooltips=[
            ("Timestamp", "@timestamp{%Y-%m-%d %H:%M:%S.%3N}"),
            ("Ticker", "@ticker"),
            ("Value", "@value{0.00}")
        ],
        formatters={
            '@timestamp': 'datetime'
        },
        mode='vline'
    )
    p.add_tools(hover)

    return p

def create_layout(plots: Dict[PlotPosition, figure]):
    overlay_plot = plots.get(PlotPosition.OVERLAY)
    below_plots = [p for pos, p in plots.items() if pos == PlotPosition.BELOW]
    side_plot = plots.get(PlotPosition.SIDE)

    if overlay_plot:
        x_range = overlay_plot.x_range
        y_range = overlay_plot.y_range
        
        for below_plot in below_plots:
            below_plot.x_range = x_range
        if side_plot:
            side_plot.y_range = y_range

    layout = []
    if overlay_plot:
        if side_plot:
            layout.append([overlay_plot, side_plot])
        else:
            layout.append([overlay_plot])
    layout.extend([[p] for p in below_plots])

    return gridplot(layout, sizing_mode="scale_width")

def save_plot(layout, filename: str):
    output_file(filename)
    save(layout)
    logger.info(f"Chart saved as HTML: {filename}")
