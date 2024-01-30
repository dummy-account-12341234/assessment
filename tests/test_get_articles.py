import unittest
import datetime

import pandas as pd

from main import get_articles


class TestGetArticles(unittest.TestCase):

    def setUp(self):
        self.df = get_articles(['brexit', 'elections'],
                               from_date=(datetime.datetime.now(
                                   ) - datetime.timedelta(days=5)),
                               to_date=datetime.datetime.now())

    def test_columns(self):
        expected_keys = ['id', 'type', 'sectionId', 'sectionName',
                         'webPublicationDate', 'webTitle', 'webUrl',
                         'apiUrl', 'isHosted', 'pillarId',
                         'pillarName', 'Wordcount']
        keys = list(self.df.keys())

        self.assertListEqual(expected_keys, keys)

    def test_row_count(self):
        # i could calculate the expected row count by querying the api
        # and checking the number_of_pages * articles_per_page
        # but i want to keep things simple and not keep the script running for
        # too long
        self.assertGreater(len(self.df), 0)


if __name__ == '__main__':
    unittest.main()