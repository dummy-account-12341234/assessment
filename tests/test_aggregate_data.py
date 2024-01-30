import unittest

from main import aggregate_data
import pandas as pd


class TestAggregateData(unittest.TestCase):

    def setUp(self):
        self.df = aggregate_data("articles.csv")
        self.articles_df = pd.read_csv('articles.csv')

    def test_columns(self):
        self.assertListEqual(list(self.df.columns), ['count', 'month',
                                                          'pillarName'])

    def test_row_count(self):
        self.assertGreater(len(self.df), 0)
        self.assertGreater(len(self.articles_df), len(self.df))
