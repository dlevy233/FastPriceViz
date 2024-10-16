from visualization.plot_base import PlotBase
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Range1d

class LinePlot(PlotBase):
    def __init__(self, title='', x_axis_label='X-Axis', y_axis_label='Y-Axis'):
        super().__init__(title, x_axis_label, y_axis_label)
        self.extra_y_ranges = {}
        self.y_range_names = []
        self.plot = figure(title=title, x_axis_label=x_axis_label, y_axis_label=y_axis_label)

    def add_line(self, source, x_axis, y_axis, color, legend_label, y_range_name=None):
        if y_range_name:
            if y_range_name not in self.extra_y_ranges:
                new_range = Range1d()
                self.extra_y_ranges[y_range_name] = new_range
                self.plot.extra_y_ranges[y_range_name] = new_range
                new_axis = LinearAxis(y_range_name=y_range_name, axis_label=legend_label)
                self.plot.add_layout(new_axis, 'right')
            y_range_name_to_use = y_range_name
        else:
            y_range_name_to_use = 'default'

        if y_range_name_to_use not in self.y_range_names:
            self.y_range_names.append(y_range_name_to_use)

        line = self.plot.line(
            x=x_axis,
            y=y_axis,
            source=source,
            color=color,
            legend_label=legend_label,
            y_range_name=y_range_name_to_use
        )
        
        self._update_y_range(source, y_axis, y_range_name_to_use)
        
        return line

    def _update_y_range(self, source, y_axis, y_range_name):
        y_values = source.data[y_axis]
        y_min, y_max = min(y_values), max(y_values)
        padding = (y_max - y_min) * 0.1
        
        if y_range_name == 'default':
            self.plot.y_range.start = y_min - padding
            self.plot.y_range.end = y_max + padding
        else:
            self.extra_y_ranges[y_range_name].start = y_min - padding
            self.extra_y_ranges[y_range_name].end = y_max + padding

    def render(self):
        # Ensure all y-ranges are properly set
        for y_range_name in self.y_range_names:
            if y_range_name != 'default':
                self.plot.extra_y_ranges[y_range_name] = self.extra_y_ranges[y_range_name]

        self.plot.legend.click_policy = "hide"  # Allow toggling lines on/off
        return self.plot
