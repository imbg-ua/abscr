subpackages = [
    'ome',
    'dataload',
    'analysis',
    'prepocessing',
    'segmentation',
    'util',
    
]

import lazy_loader as lazy
__getattr__, __dir__, _ = lazy.attach(__name__, subpackages)