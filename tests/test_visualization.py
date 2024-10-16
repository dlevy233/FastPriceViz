import unittest
from visualization.line_plot import LinePlot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure as Figure
import pandas as pd

class TestLinePlot(unittest.TestCase):
    def setUp(self):
        self.line_plot = LinePlot(title='Test Plot', x_axis_label='X', y_axis_label='Y')
        self.data = pd.DataFrame({
            'timestamp': pd.date_range(start='2024-05-01', periods=100, freq='s'),
            'price': range(100)
        })
        self.source = ColumnDataSource(self.data)

    def test_add_line(self):
        line = self.line_plot.add_line(self.source, 'timestamp', 'price', 'blue', 'Test Line')
        self.assertIsNotNone(line)

    def test_multiple_y_axes(self):
        self.line_plot.add_line(self.source, 'timestamp', 'price', 'blue', 'Test Line 1')
        self.line_plot.add_line(self.source, 'timestamp', 'price', 'red', 'Test Line 2', y_range_name='y2')
        
        rendered = self.line_plot.render()
        self.assertEqual(len(rendered.yaxis), 2)

    def test_render(self):
        self.line_plot.add_line(self.source, 'timestamp', 'price', 'blue', 'Test Line')
        rendered = self.line_plot.render()
        self.assertIsInstance(rendered, Figure)

if __name__ == '__main__':
    unittest.main()
