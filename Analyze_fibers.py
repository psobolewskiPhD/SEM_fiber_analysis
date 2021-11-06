# %%
# Import needed libraries and modules
import os

import dask
import numpy as np
from dask import delayed
from dask_image.imread import imread
from quanfima import morphology as mrph
from skimage import filters, morphology

# %%
# Use dask to read the image files, which permits for lazy loading.
all_samples = imread("./fiber_data/*.jpg")
# set the scale in micron per pixel of the images
scale = [1 / 35.5, 1 / 35.5]
# get list of filenames to match the imported images, ignore dot files
file_list = []
for item in os.listdir("fiber_data"):
    if not item.startswith(".") and os.path.isfile(os.path.join("fiber_data", item)):
        file_list.append(item)
file_list = sorted(file_list)

# %%
# Ensure images are grayscale
def grayscale(rgb):
    gray = (rgb[..., 0] * 0.2125) + (rgb[..., 1] * 0.7154) + (rgb[..., 2] * 0.0721)
    return gray


all_samples = grayscale(all_samples)

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


# Using dask `map_block` the segmentation
# The function `segment_img` is applied blockwise to `all_samples`
seg = all_samples.map_blocks(segment_img, dtype=np.uint8)
# Do the actual computations
seg_stack = seg.compute()

# %%
# Define function to use quanfima to calculate porosity
# The input is a segmented image
def porosity(seg_slice):
    pr = mrph.calc_porosity(seg_slice)
    porosity_val = pr["Material 1"]
    return porosity_val


# %%
# Using dask delayed the porosity function will be run on each img
# The values will be appended to a list `porosity_out`
porosity_out = []

for sample in seg_stack:
    por_vals = delayed(porosity)(sample)
    porosity_out.append(por_vals)

# %%
# Compute the porosity values
# Note you may wish to use additional workers
# or a different scheduler. See:
# https://docs.dask.org/en/latest/scheduler-overview.html
porosity_c = dask.compute(*porosity_out)

# Make a dict pairing up the names of the files with the values
porosity_dict = dict(zip(file_list, porosity_c))

# %%
# Define function to use quanfima to calculate porosity
# The input is a segmented image
def fiber_analysis(seg_slice):
    # first the image is skeletonized using skimage
    skel = morphology.skeletonize(seg_slice)
    # quanfima function to get fiber parameters
    cskel, fskel, omap, dmap, ovals, dvals = mrph.estimate_fiber_properties(
        seg_slice, skel, window_radius=3
    )
    # return a list of the orientation and diameter arrays
    fvals = [ovals, dvals]
    return fvals


# %%
# Using dask delayed the analysis function will be run on each img
# The values will be appended to a list `fvals_out`
fvals_out = []

for sample in seg_stack:
    fvals = delayed(fiber_analysis)(sample)
    fvals_out.append(fvals)


# %%
# Compute the fiber parameters.
# Note: this can take ~1 min per image
# You may wish to use additional workers
# or a different scheduler. See:
# https://docs.dask.org/en/latest/scheduler-overview.html
fvals_c = dask.compute(*fvals_out)
# %%
# Iterate over samples to compute means and st_devs
f_out = []

for sample in fvals_c:
    ovals = sample[0]
    o_m_s = [np.mean(ovals), np.std(ovals)]
    dvals = sample[1]
    d_m_s = [np.mean(dvals), np.std(dvals)]
    f_o = [o_m_s, d_m_s]
    f_out.append(f_o)

# Make a dict pairing up the names of the files with the values
# File name: [orientation_mean, std], [diameter_mean, std]
# Note the orientation values are radians, diameters in pixels
f_out_dict = dict(zip(file_list, f_out))

# %%
