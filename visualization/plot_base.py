from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

class PlotBase:
    def __init__(self, title='', x_axis_label='X-Axis', y_axis_label='Y-Axis'):
        self.figure = figure(title=title, x_axis_type='datetime')
        self.figure.xaxis.axis_label = x_axis_label
        self.figure.yaxis.axis_label = y_axis_label
        self.data_sources = []

    def add_plot(self, data_source, x='x', y='y', plot_type='line', **kwargs):
        """
        Add a new plot to the existing figure.
        :param data_source: ColumnDataSource containing the data to plot
        :param x: Name of the column to use for x-axis data
        :param y: Name of the column to use for y-axis data
        :param plot_type: Type of plot to add ('line', 'scatter', etc.)
        :param kwargs: Additional keyword arguments for customizing the plot (e.g., color, legend_label)
        """
        self.data_sources.append((data_source, x, y, plot_type, kwargs))

    def render(self):
        for data_source, x, y, plot_type, kwargs in self.data_sources:
            if plot_type == 'line':
                self.figure.line(x=x, y=y, source=data_source, **kwargs)
            elif plot_type == 'scatter':
                self.figure.scatter(x=x, y=y, source=data_source, **kwargs)
            # Add more plot types as needed

        return self.figure
