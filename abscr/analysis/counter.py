'''Implementation of counting of a cell masks from NN'''

import logging
import os
import numpy as np
from typing import Union
from cellpose import utils

class CellCounter:
    def __init__(self) -> None:
        pass
    
    def count_cells_buccal(self, buccal_swab_segm: 'BuccalSwabSegmentation'):
        result = self.count_cells_from_masks(buccal_swab_segm.epithelial_masks, buccal_swab_segm.immune_masks)
        
        # immune cells segmentation is yet to be implemented
        # dummy_result = (result[0], np.clip(np.round(np.random.normal(0.21 * result[0], 0.07 * result[0])).astype(int), 0, None))
        
        return result
        
    def count_cells_from_masks(self, *masks) -> Union[tuple, int]:
        result_counts = []
        
        for masks_array in masks:
            cells_count = None
            if isinstance(masks_array, np.ndarray):
                cells_count = len(utils.outlines_list(masks_array)) 
            elif isinstance(masks_array, str):          
                ext_name = os.path.splitext(os.path.basename(masks_array))[1]
                if ext_name == '.txt':
                    cells_count = len(open(masks_array).readlines())
                elif ext_name == '.npy':
                    dat = np.load(masks_array, allow_pickle=True).item()
                    outlines = utils.outlines_list(dat['masks'])
                    cells_count = len(outlines)
                else:
                    logging.error(f'{masks_array} has incorrect file format')
                    raise ValueError('Incorrect file format. Either a .txt or a .npy file with masks must be passed')
                    
            result_counts.append(cells_count)
                            
        if len(result_counts) == 1:
            return result_counts[0]
        else:
            return tuple(result_counts)