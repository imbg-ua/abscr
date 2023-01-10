import unittest
import sys
sys.path.append('../')
from abscr import im
from abscr.abscr.dataload.data_loader import DataLoader


class TestDataloader(unittest.TestCase):
    def runTest(self):
        loader = DataLoader()
        self.assertEqual(loader.test_data_url, 'https://git.github.com/asdas/asda/test_example.pkl', 'URLs mismatch')


unittest.main()
