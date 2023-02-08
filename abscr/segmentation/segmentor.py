import logging
import traceback
import os
import numpy as np
import matplotlib.pyplot as plt
import PIL
from cellpose import models, core, io, plot, utils

class Segmentor:
    def __init__(self) -> None:
        self.models = ['cellpose']
        logging.info(f'Available models:\n{self.models}')
        pass

    def predict(self, image, diameter=65, flow_threshold=None, channels=[0, 0], invert=True, model_type='cyto', plot_segmentation=False, savedir=None):
        
        if isinstance(image, PIL.Image.Image):
            PIL_image = image
        else:
            try:                
                PIL_image = PIL.Image.open(image)
            except:
                logging.error(traceback.format_exc())
                return 
                
        if savedir is None:
            savedir = os.getcwd()    
            
        io.check_dir(savedir)
        basename = os.path.splitext(os.path.basename(PIL_image.filename))[0] + '_epithelial'
            
        image_array = np.asarray(PIL_image)
        
        model = models.Cellpose(model_type=model_type, gpu=core.use_gpu())
        masks, flows, styles, diams = model.eval(image_array, diameter=diameter,
                                                 flow_threshold=flow_threshold,
                                                 channels=channels,
                                                 invert=invert)
        
        outlines = utils.outlines_list(masks)
        io.outlines_to_text(os.path.join(savedir, basename), outlines)
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 5), dpi=200, facecolor='white')
        [axi.set_axis_off() for axi in ax.ravel()]
        fig.suptitle(f'{basename} segmentation')
        
        ax[0].imshow(image_array)
        overlay = plot.mask_overlay(image_array, masks)
        ax[1].imshow(overlay)
        
        fig.savefig(os.path.join(savedir, basename + '.png'), dpi=fig.dpi, bbox_inches='tight')
        
        if plot_segmentation:
            plt.show()
        plt.close()
        
        return masks, flows, styles, diams