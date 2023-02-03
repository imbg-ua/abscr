import logging
import traceback
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models, core, io, plot
import PIL

class Segmentor:
    def __init__(self) -> None:
        self.models = ['cellpose']
        logging.info(f'Available models:\n{self.models}')
        pass

    def predict(self, image, diameter=65, flow_threshold=None, channels=[0, 0], invert=True, model_type='cyto', plot_segmentation=False):
        
        if isinstance(image, PIL.Image.Image):
            PIL_image = image
        else:
            try:
                PIL_image = PIL.Image.open(image)
            except:
                logging.error(traceback.format_exc())
                return 
                
                
        image_array = np.asarray(PIL_image)
        
        model = models.Cellpose(model_type=model_type, gpu=core.use_gpu())
        masks, flows, styles, diams = model.eval(image_array, diameter=diameter,
                                                 flow_threshold=flow_threshold,
                                                 channels=channels,
                                                 invert=invert)
        
        io.save_masks(image_array, masks, flows, 'epithelial_segmentation', png=False, tif=False) 
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 5), dpi=200, facecolor='white')
        [axi.set_axis_off() for axi in ax.ravel()]
        fig.suptitle('Epithelial cells segmentation')
        
        ax[0].imshow(image_array)
        overlay = plot.mask_overlay(image_array, masks)
        ax[1].imshow(overlay)
        
        fig.savefig('epithelial_segmentation.png', dpi=fig.dpi, bbox_inches='tight')
        
        if plot_segmentation:
            plt.show()
        plt.close()
        
        return masks, flows, styles, diams