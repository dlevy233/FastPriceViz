from bokeh.plotting import figure

class LinePlot:
    def __init__(self, title='', x_axis='timestamp', y_axis='price', data_source=None):
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.data_source = data_source
        self.figure = figure(title=title, x_axis_type='datetime')

    def render(self):
        data = self.data_source.data.compute()
        if self.x_axis == data.index.name:
            x = data.index
        else:
            x = data[self.x_axis]
        y = data[self.y_axis]
        self.figure.line(x, y)
        return self.figure
