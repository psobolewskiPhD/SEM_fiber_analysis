# %%
# Import needed libraries and modules

import napari
import numpy as np
from dask_image.imread import imread
from skimage import filters, morphology

# %%
# Use dask to read the image files, which permits for lazy loading.
all_samples = imread("./fiber_data/*.jpg")
# set the scale in micron per pixel of the images
scale = [1 / 35.5, 1 / 35.5]
# %%
# Ensure images are grayscale
def grayscale(rgb):
    gray = (rgb[..., 0] * 0.2125) + (rgb[..., 1] * 0.7154) + (rgb[..., 2] * 0.0721)
    return gray


all_samples = grayscale(all_samples)
# %%
# Initialize napari viewer and show the Image stack
viewer = napari.Viewer()
viewer.add_image(all_samples, scale=scale, name="Images")

# %%
# Define segmentation function. The input is an image stack
def segment_img(img_stack):
    # ensure lead dimension is dropped, so just one slice, a 2D image is passed
    slice = img_stack[0, ...]
    # crop out the bottom, where the SEM info is located
    crop = slice[
        0:890,
    ]
    # Use skimage Niblack thresholding algorithm
    # Can change this to preview a different one method.
    thresh = filters.threshold_niblack(crop)
    seg = (crop > thresh).astype(np.uint8)
    # restore the missing dimension to make a stack again
    return seg[None, ...]


# %%
# Define skeleton function, use result of the segmentation
def skel_img(seg_stack):
    slice = seg_stack[0, ...]
    skeleton = morphology.skeletonize(slice)
    skeleton = skeleton.astype(np.uint8)
    return skeleton[None, ...]


# %%
# Using dask `map_block` the segmentation
# The function `segment_img` is applied blockwise to `all_samples`
# Now it is lazy: not computed until called
seg = all_samples.map_blocks(segment_img, dtype=np.uint8)

# View lazy segmentation napari
viewer.add_labels(seg, scale=scale, name="Segmentation")

# %%
# Using dask `map_block` the skeletonization
# The function `skel_img` is applied blockwise to `seg`
# Now it is lazy: applied block-wise, but not computed until called
skel = seg.map_blocks(skel_img, dtype=np.uint8)

# View lazy skeleton napari
# Use `Shuffle colors` crossed-arrows icon to swap the color for improved contrast
viewer.add_labels(skel, scale=scale, name="Skeleton")
# %%
