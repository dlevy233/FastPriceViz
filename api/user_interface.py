from bokeh.io import show
from bokeh.layouts import column, row
from bokeh.models import Range1d

class Figure:
    def __init__(self):
        self.plots = []

    def add_plot(self, plot, position='overlap'):
        self.plots.append((plot, position))

    def show(self, return_layout=False):
        overlapped_plots = []
        below_plots = []
        side_plots = []

        for plot, position in self.plots:
            if position == 'overlap':
                overlapped_plots.append(plot)
            elif position == 'below':
                below_plots.append(plot)
            elif position == 'side':
                side_plots.append(plot)

        rendered_plots = []

        if overlapped_plots:
            base_plot = overlapped_plots[0].render()
            for plot in overlapped_plots[1:]:
                rendered = plot.render()
                base_plot.add_layout(rendered.yaxis[0], 'right')
                base_plot.extra_y_ranges.update(rendered.extra_y_ranges)
                base_plot.renderers.extend(rendered.renderers)
            rendered_plots.append(base_plot)

        rendered_plots.extend([plot.render() for plot in below_plots])

        main_column = column(*rendered_plots) if rendered_plots else None

        if side_plots:
            side_rendered = column(*[plot.render() for plot in side_plots])
            layout = row(main_column, side_rendered) if main_column else side_rendered
        else:
            layout = main_column

        if return_layout:
            return layout
        else:
            show(layout)
