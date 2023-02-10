import logging
import traceback
import os
import numpy as np
import matplotlib.pyplot as plt
import PIL
from cellpose import models, core, io, plot, utils


class BuccalSegmentation:
    def __init__(self, epithelial_masks, epithelial_flows, epithelial_styles, epithelial_diams, 
                immune_masks, immune_flows, immune_styles, immune_diams):
        
        # dataclass?
        self.epithelial_masks = epithelial_masks
        self.epithelial_flows = epithelial_flows
        self.epithelial_styles = epithelial_styles
        self.epithelial_diams = epithelial_diams
        
        self.immune_masks = immune_masks
        self.immune_flows = immune_flows
        self.immune_styles = immune_styles
        self.immune_diams = immune_diams


class Segmentor:
    def __init__(self) -> None:
        self.models = ['cellpose']
        logging.info(f'Available models:\n{self.models}')
        pass
    
    def check_image(self, image):
        if isinstance(image, PIL.Image.Image):
            return image
        else:
            try:                
                PIL_image = PIL.Image.open(image)
            except:
                logging.error(traceback.format_exc())
                return
            return PIL_image
            
    def predict_epithelial(self, image, diameter=65, flow_threshold=None, channels=[0, 0], invert=True, model_type='cyto'):
        if isinstance(image, np.ndarray):
            image_array = image
        else:
            PIL_image = self.check_image(image)
            image_array = np.asarray(PIL_image)
        
        model = models.Cellpose(model_type=model_type, gpu=core.use_gpu())
        masks, flows, styles, diams = model.eval(image_array, diameter=diameter,
                                                 flow_threshold=flow_threshold,
                                                 channels=channels,
                                                 invert=invert)
        return masks, flows, styles, diams
    
    def predict_immune(self, image, diameter=6, flow_threshold=0.4, channels=[0, 0], invert=True, model_type='cyto2'):
        if isinstance(image, np.ndarray):
            image_array = image
        else:
            PIL_image = self.check_image(image)
            image_array = np.asarray(PIL_image)
        
        model = models.Cellpose(model_type=model_type, gpu=core.use_gpu())
        masks, flows, styles, diams = model.eval(image_array, diameter=diameter,
                                                 flow_threshold=flow_threshold,
                                                 channels=channels,
                                                 invert=invert)
        
        return masks, flows, styles, diams

    def predict_all(self, image, plot_segmentation=False, savedir=None):
        PIL_image = self.check_image(image)
        image_array = np.asarray(PIL_image)
        basename = os.path.splitext(os.path.basename(PIL_image.filename))[0]
        
        epithelial_masks, epithelial_flows, epithelial_styles, epithelial_diams = self.predict_epithelial(image_array)
        # immune_masks, immune_flows, immune_styles, immune_diams = self.predict_immune(image_array)
        immune_masks, immune_flows, immune_styles, immune_diams = epithelial_masks, epithelial_flows, epithelial_styles, epithelial_diams
        
        if savedir is None:
            savedir = os.getcwd()  
        io.check_dir(savedir)
        
        self.save_txt_masks([epithelial_masks, immune_masks], basename=basename, savedir=savedir)
        if plot_segmentation:
            # immune masks will be plotted too
            self.plot_segmentation(image_array, [epithelial_masks], basename=basename, save_png=True, savedir=savedir)
            
        return BuccalSegmentation(epithelial_masks, epithelial_flows, epithelial_styles, epithelial_diams, immune_masks, immune_flows, immune_styles, immune_diams)
    
    
    def plot_segmentation(self, image, masks_array, basename=None, save_png=False, savedir=None):
        if isinstance(image, np.ndarray):
            image_array = image
            if basename is None:
                raise ValueError('When passing an image as np.ndarray, the file basename must be specified.')
                return
            basename = basename
        else:
            PIL_image = self.check_image(image)
            image_array = np.asarray(PIL_image)
            basename = os.path.splitext(os.path.basename(PIL_image.filename))[0]     
                
        fig, ax = plt.subplots(1, len(masks_array) + 1, figsize=(12, 5), dpi=200, facecolor='white')
        [axi.set_axis_off() for axi in ax.ravel()]
        fig.suptitle(f'{basename} segmentation')
        ax[0].imshow(image_array)
         
        for i in range(1, len(ax)):
            overlay = plot.mask_overlay(image_array, masks_array[i - 1])
            ax[i].imshow(overlay)
        
        if save_png:
            if savedir is None:
                savedir = os.getcwd()  
            io.check_dir(savedir)
            fig.savefig(os.path.join(savedir, basename + '_segmentation.png'), dpi=fig.dpi, bbox_inches='tight')
            
        plt.show()
        plt.close()
        
    def save_txt_masks(self, masks_array, basename, savedir=None):
        for i in range(len(masks_array)):
            outlines = utils.outlines_list(masks_array[i])
            io.outlines_to_text(os.path.join(savedir, basename + '_' + str(i + 1)), outlines)