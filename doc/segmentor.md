Documentation for the classes and methods:

The code defines three classes: `SegmentationData`, `BuccalSwabSegmentation`, and `Segmentor`.

`SegmentationData` is a simple class that contains information about segmentation data, such as masks, flows, styles, and diams. The constructor initializes these variables to None but can be updated later.

`BuccalSwabSegmentation` class represents the result of epithelial and immune segmentation of a buccal swab image. The class takes two parameters: `epithelial_segm_result` and `immune_segm_result`. It sets four variables for each of these two parameters: `epithelial_masks`, `epithelial_flows`, `epithelial_styles`, and `epithelial_diams` for epithelial segmentation, and `immune_masks`, `immune_flows`, `immune_styles`, and `immune_diams` for immune segmentation. These variables contain the segmentation data, and they can be accessed later by the user.

`Segmentor` is the main class that performs the image segmentation using the Cellpose model. The constructor initializes the list of available models (in this case, only the Cellpose model). It has three methods:

- `check_image(image)` takes an image and returns a PIL image object if the input is not already a PIL image. Otherwise, it returns the input image.

- `predict_epithelial(image, diameter, flow_threshold, cellprob_threshold, channels, invert, model_type, batch_size)` takes an image and uses the Cellpose model to predict the epithelial segmentation. It returns a `SegmentationData` object that contains the segmentation masks, flows, styles, and diams.

- `predict_immune(image, diameter, flow_threshold, cellprob_threshold, channels, invert, model_type, batch_size)` is not yet implemented but will perform immune cell segmentation.

- `predict_all(image, diameter_epithelial, flow_threshold_epithelial, cellprob_threshold_epithelial, channels_epithelial, invert_epithelial, model_type_epithelial, diameter_immune, flow_threshold_immune, cellprob_threshold_immune, channels_immune, invert_immune, model_type_immune, batch_size, save_png, plot_segm, savedir, basename)` is the main method that performs epithelial and immune cell segmentation on an input image. The method takes several parameters, including `image`, `diameter_epithelial`, `flow_threshold_epithelial`, `cellprob_threshold_epithelial`, `channels_epithelial`, `invert_epithelial`, and `model_type_epithelial` for epithelial segmentation and similar parameters for immune cell segmentation. If `save_png` is True, the method saves the segmented image as a PNG file. If `plot_segm` is True, the method plots the segmentation and displays it on the screen. The method returns a `BuccalSwabSegmentation` object that contains the segmentation results for epithelial and immune cells.

- `plot_segmentation(image, masks_array, basename, save_png, savedir, plot_segm)` is a helper function that takes an image and an array of masks, plots the image and the masks on a figure, and saves it as a PNG file if `save_png` is True.

- `save_txt_masks(self, masks_array, basename, savedir=None)` is a function that takes three arguments: `masks_array`, `basename`, and `savedir`. The `masks_array ` parameter is a list of binary masks, where each mask is a 2D numpy array of zeros and ones. The `basename` parameter is a string that represents the base name of the output file, and the `savedir` parameter is an optional string that represents the directory where the output file will be saved. If the `savedir` parameter is not provided, the output file will be saved in the current working directory.