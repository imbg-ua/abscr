import logging
import traceback
import os
import numpy as np
import matplotlib.pyplot as plt
import PIL
from cellpose import models, core, io, plot, utils

class SegmentationData:
    def __init__(self, masks=None, flows=None, styles=None, diams=None):
        self.masks = masks
        self.flows = flows
        self.styles = styles
        self.diams = diams
        

class BuccalSwabSegmentation:
    def __init__(self, epithelial_segm_result, immune_segm_result):
        self.epithelial_masks = epithelial_segm_result.masks
        self.epithelial_flows = epithelial_segm_result.flows
        self.epithelial_styles = epithelial_segm_result.styles
        self.epithelial_diams = epithelial_segm_result.diams
        
        self.immune_masks = immune_segm_result.masks
        self.immune_flows = immune_segm_result.masks
        self.immune_styles = immune_segm_result.masks
        self.immune_diams = immune_segm_result.masks


class Segmentor:
    def __init__(self) -> None:
        self.models = ['cellpose']
        logging.info(f'Available models:\n{self.models}')
        pass
    
    @staticmethod
    def check_image(image):
        if isinstance(image, PIL.Image.Image):
            return image
        else:
            try:                
                PIL_image = PIL.Image.open(image)
            except:
                logging.error(traceback.format_exc())
                return
            return PIL_image
            
    def predict_epithelial(self, image, diameter=30, flow_threshold=0.4, cellprob_threshold=0.0,
                           channels=[0, 0], invert=True, model_type='cyto', batch_size=8):
        if isinstance(image, np.ndarray):
            image_array = image
        else:
            PIL_image = self.check_image(image)
            image_array = np.asarray(PIL_image)
        
        model = models.Cellpose(model_type=model_type, gpu=core.use_gpu())
        masks, flows, styles, diams = model.eval(image_array, diameter=diameter,
                                                 flow_threshold=flow_threshold,
                                                 cellprob_threshold=cellprob_threshold,
                                                 channels=channels,
                                                 invert=invert,
                                                 batch_size=batch_size)
        return SegmentationData(masks, flows, styles, diams)
    
    # to be implemented
    def predict_immune(self, image, diameter, flow_threshold, cellprob_threshold,
                       channels, invert, model_type, batch_size):
        pass

    def predict_all(self, image, diameter_epithelial=30, flow_threshold_epithelial=0.4, cellprob_threshold_epithelial=0.0,
                    channels_epithelial=[0, 0], invert_epithelial=True, model_type_epithelial='cyto',
                    diameter_immune=None, flow_threshold_immune=None, cellprob_threshold_immune=None,
                    channels_immune=None, invert_immune=None, model_type_immune=None,
                    batch_size=8, save_png=True, plot_segm=False, savedir=None, basename=None):
        if isinstance(image, np.ndarray):
            image_array = image
            if basename is None and save_png:
                raise ValueError('When passing an image as np.ndarray, the file basename must be specified.')
                return
            basename = basename
        else:
            PIL_image = self.check_image(image)
            image_array = np.asarray(PIL_image)
            if basename is not None:
                basename = basename
            else:
                basename = os.path.splitext(os.path.basename(PIL_image.filename))[0]
        
        
        epithelial_segmentation = self.predict_epithelial(image_array, diameter=diameter_epithelial,
                                                          flow_threshold=flow_threshold_epithelial,
                                                          cellprob_threshold=cellprob_threshold_epithelial,
                                                          channels=channels_epithelial, invert=invert_epithelial,
                                                          model_type=model_type_epithelial, batch_size=batch_size)
        
        # immune segmentation is to be implemented
        immune_segmentation = SegmentationData()
        
        if savedir is None:
            savedir = os.getcwd()  
        io.check_dir(savedir)
        
        self.save_txt_masks([epithelial_segmentation.masks], basename=basename, savedir=savedir)
        self.plot_segmentation(image_array, [epithelial_segmentation.masks], basename=basename,
                               savedir=savedir, save_png=save_png, plot_segm=plot_segm)
            
        return BuccalSwabSegmentation(epithelial_segmentation, immune_segmentation)
    
    
    def plot_segmentation(self, image, masks_array, basename=None, save_png=False, savedir=None, plot_segm=True):
        if not (save_png or plot_segm):
            return

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

        plt.ioff()
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
            
        if plot_segm:
            plt.show()
        plt.close()
        
    def save_txt_masks(self, masks_array, basename, savedir=None):
        if len(masks_array) == 1:
            outlines = utils.outlines_list(masks_array[0])
            io.outlines_to_text(os.path.join(savedir, basename), outlines)
        else:
            for i in range(len(masks_array)):
                outlines = utils.outlines_list(masks_array[i])
                io.outlines_to_text(os.path.join(savedir, basename + '_' + str(i + 1)), outlines)
