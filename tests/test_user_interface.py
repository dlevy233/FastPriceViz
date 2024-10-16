import unittest
from api.user_interface import Figure
from visualization.line_plot import LinePlot
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, LayoutDOM
import pandas as pd

class TestFigure(unittest.TestCase):
    def setUp(self):
        self.figure = Figure()
        self.data = pd.DataFrame({
            'timestamp': pd.date_range(start='2024-05-01', periods=100, freq='s'),
            'price': range(100)
        })
        self.source = ColumnDataSource(self.data)

    def create_plot(self):
        plot = LinePlot(title='Test Plot', x_axis_label='X', y_axis_label='Y')
        plot.add_line(self.source, 'timestamp', 'price', 'blue', 'Test Line')
        return plot

    def test_add_plot(self):
        plot = self.create_plot()
        self.figure.add_plot(plot, position='overlap')
        self.assertEqual(len(self.figure.plots), 1)

    def test_show_overlap(self):
        plot1 = self.create_plot()
        plot2 = self.create_plot()
        self.figure.add_plot(plot1, position='overlap')
        self.figure.add_plot(plot2, position='overlap')
        layout = self.figure.show(return_layout=True)
        self.assertIsInstance(layout, LayoutDOM)

    def test_show_below(self):
        plot1 = self.create_plot()
        plot2 = self.create_plot()
        self.figure.add_plot(plot1, position='below')
        self.figure.add_plot(plot2, position='below')
        layout = self.figure.show(return_layout=True)
        self.assertIsInstance(layout, LayoutDOM)

    def test_show_side(self):
        plot1 = self.create_plot()
        plot2 = self.create_plot()
        self.figure.add_plot(plot1, position='side')
        self.figure.add_plot(plot2, position='side')
        layout = self.figure.show(return_layout=True)
        self.assertIsInstance(layout, LayoutDOM)

    def test_mixed_layout(self):
        plot1 = self.create_plot()
        plot2 = self.create_plot()
        plot3 = self.create_plot()
        self.figure.add_plot(plot1, position='overlap')
        self.figure.add_plot(plot2, position='below')
        self.figure.add_plot(plot3, position='side')
        layout = self.figure.show(return_layout=True)
        self.assertIsInstance(layout, LayoutDOM)

if __name__ == '__main__':
    unittest.main()
