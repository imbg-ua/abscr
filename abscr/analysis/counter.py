'''Implementation of counting of a cell masks from NN'''

import logging
import os
import numpy as np
from typing import Union
from cellpose import utils


class CellCounter:
    def __init__(self) -> None:
        pass

    def count_cells(self, epithelial_masks=None, immune_masks=None) -> Union[tuple, int]:
        # TODO: better error handling
        epithelial_count = None
        if isinstance(epithelial_masks, np.ndarray):
            epithelial_count = len(utils.outlines_list(epithelial_masks)) 
        elif isinstance(epithelial_masks, str):          
            ext_name = os.path.splitext(os.path.basename(epithelial_masks))[1]
            if ext_name == '.txt':
                epithelial_count = len(open(epithelial_masks).readlines())
            elif ext_name == '.npy':
                dat = np.load(epithelial_masks, allow_pickle=True).item()
                outlines = utils.outlines_list(dat['masks'])
                epithelial_count = len(outlines)
            else:
                logging.error(f'{epithelial_masks} has incorrect file format')
                raise ValueError('Incorrect file format. Either a .txt or a .npy file with masks must be passed')
                
        
        immune_count = None
        if isinstance(immune_masks, np.ndarray):
            immune_count = len(utils.outlines_list(immune_masks)) 
        elif isinstance(immune_masks, str):          
            ext_name = os.path.splitext(os.path.basename(immune_masks))[1]
            if ext_name == '.txt':
                immune_count = len(open(immune_masks).readlines())
            elif ext_name == '.npy':
                dat = np.load(immune_masks, allow_pickle=True).item()
                outlines = utils.outlines_list(dat['masks'])
                immune_count = len(outlines)
            else:
                logging.error(f'{immune_masks} has incorrect file format')
                raise ValueError('Incorrect file format. Either a .txt or a .npy file with masks must be passed')
        
        # dummy
        # note that epithelial_count must be not None here
        if immune_masks is not None:
            immune_count = np.clip(np.round(np.random.normal(0.21 * epithelial_count, 0.07 * epithelial_count)).astype(int), 0, None)
        
        if epithelial_count is not None and immune_count is not None:
            # print(f'Epithelial cells count: {epithelial_count}\nImmune cells count: {immune_count}')
            return (epithelial_count, immune_count)
        elif epithelial_count is not None:
            return epithelial_count
        elif immune_count is not None:
            return immune_count
        else:
            raise ValueError("Bad arguments. Couldn't count the cells")
            
        
            
                
                
        
