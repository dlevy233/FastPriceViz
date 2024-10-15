from bokeh.io import show
from bokeh.layouts import column

class Figure:
    def __init__(self):
        self.plots = []

    def add_plot(self, plot, position='overlap'):
        self.plots.append((plot, position))

    def show(self):
        figures = [plot.render() for plot, _ in self.plots]
        layout = column(*figures)
        show(layout)
