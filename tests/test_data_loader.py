import unittest
import sys
sys.path.append('../')
from abscr.abscr.dataload.data_loader import DataLoader
from abscr.abscr.analysis.counter import CellCounter


class TestDataloader(unittest.TestCase):
    def runTest(self):
        loader = DataLoader()
        self.assertEqual(loader.test_data_url, 'https://git.github.com/asdas/asda/test_example.pkl', 'URLs mismatch')
        self.assertEqual(loader.load_test_data().status_code, 200, 'Failed request')

        cc = CellCounter()
        self.assertEqual(cc.count_cells([]), -1, 'Cell counter does not work properly')


unittest.main()
