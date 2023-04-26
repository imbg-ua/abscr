import unittest
import numpy as np
import sys
# TODO: refactor imports
sys.path.append('../abscr')
from abscr.analysis import counter

class TestCellCounter(unittest.TestCase):
    def setUp(self):
        self.counter = counter.CellCounter()

    def test_count_cells_from_masks_with_numpy_array(self):
        # Test with a numpy array of masks
        masks_array = np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]])
        expected_count = 2
        result = self.counter.count_cells_from_masks(masks_array)
        self.assertEqual(result, expected_count)

    def test_count_cells_from_masks_with_txt_file(self):
        # Test with a text file containing masks
        masks_file = 'test_masks.txt'
        with open(masks_file, 'w') as f:
            f.write('0 0 1 1\n0 1 1 0\n1 1 0 0\n')
        expected_count = 3
        result = self.counter.count_cells_from_masks(masks_file)
        self.assertEqual(result, expected_count)
    
    def test_count_cells_from_masks_with_npy_file(self):
        # Test with a numpy .npy file containing masks
        masks_file = 'test_masks.npy'
        masks_array = np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]])
        np.save(masks_file, {'masks': masks_array})
        expected_count = 2
        result = self.counter.count_cells_from_masks(masks_file)
        self.assertEqual(result, expected_count)

    def test_count_cells_from_masks_with_incorrect_file_format(self):
        # Test with an incorrect file format
        masks_file = 'test_masks.txtt'
        with self.assertRaises(ValueError):
            self.counter.count_cells_from_masks(masks_file)

if __name__ == '__main__':
    unittest.main()