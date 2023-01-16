import unittest
import sys
# TODO: refactor imports
sys.path.append('../abscr')
from abscr.analysis import counter
from abscr.dataload import data_loader


class TestDataloader(unittest.TestCase):
    def runTest(self):
        loader = data_loader.DataLoader()
        self.assertEqual(loader.test_data_url, 'https://git.github.com/asdas/asda/test_example.pkl', 'URLs mismatch')
        self.assertEqual(loader.load_test_data().status_code, 200, 'Failed request')

        cc = counter.CellCounter()
        self.assertEqual(cc.count_cells([]), -1, 'Cell counter does not work properly')


unittest.main()
