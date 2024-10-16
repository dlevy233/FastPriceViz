from visualization.plot_base import PlotBase
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Range1d, Legend, LegendItem

class LinePlot(PlotBase):
    def __init__(self, title='', x_axis_label='X-Axis', y_axis_label='Y-Axis'):
        super().__init__(title, x_axis_label, y_axis_label)
        self.extra_y_ranges = {}
        self.y_range_names = []
        self.plot = figure(title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)
        self.legend = Legend(click_policy="hide", location="top_left")
        self.plot.add_layout(self.legend)

    def add_line(self, source, x_axis, y_axis, color, legend_label, y_range_name=None):
        y_range_name = y_range_name or 'default'

        if y_range_name not in self.y_range_names:
            self.y_range_names.append(y_range_name)
            if y_range_name != 'default':
                new_range = Range1d()
                self.extra_y_ranges[y_range_name] = new_range
                self.plot.extra_y_ranges[y_range_name] = new_range
                new_axis = LinearAxis(y_range_name=y_range_name)
                self.plot.add_layout(new_axis, 'right')

        line = self.plot.line(
            x=x_axis,
            y=y_axis,
            source=source,
            color=color,
            y_range_name=y_range_name
        )
        
        # Create a LegendItem instead of a tuple
        legend_item = LegendItem(label=legend_label, renderers=[line])
        self.legend.items.append(legend_item)
        
        self._update_y_range(source, y_axis, y_range_name)
        
        return line

    def _update_y_range(self, source, y_axis, y_range_name):
        y_values = source.data[y_axis]
        y_min, y_max = min(y_values), max(y_values)
        padding = (y_max - y_min) * 0.1
        
        range_to_update = self.plot.y_range if y_range_name == 'default' else self.extra_y_ranges[y_range_name]
        range_to_update.start = y_min - padding
        range_to_update.end = y_max + padding

    def render(self):
        for y_range_name, y_range in self.extra_y_ranges.items():
            self.plot.extra_y_ranges[y_range_name] = y_range
        return self.plot
