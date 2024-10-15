from bokeh.plotting import figure

class PlotBase:
    def __init__(self, title=''):
        self.figure = figure(title=title, x_axis_type='datetime')

    def render(self, data_source):
        raise NotImplementedError
