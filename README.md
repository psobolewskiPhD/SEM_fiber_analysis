# SEM_fiber_analysis
This repository contains python scipts to perform fiber analysis in SEM images.
It uses [scikit-image](https://github.com/scikit-image/scikit-image) and [quanfima](https://github.com/rshkarin/quanfima)[^1] for the analysis, [dask](https://github.com/dask/dask) for lazy-loading and parallelization, and [napari](https://github.com/napari/napari) for intermediate outcome visualization.

# Step-by-step example workflow
The Jupyter notebook [`Example_Fiber_analysis.ipynb`](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Example_Fiber_analysis.ipynb) provides a step-by-step example of the image analysis workflow, using a representative SEM of bacterial cellulose fibers, provided in the [`fiber_data` folder](https://github.com/psobolewskiPhD/SEM_fiber_analysis/tree/main/fiber_data). An exported [PDF version](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Example_Fiber_analysis.pdf) is also provided.

# Visualizing the segmentation and skeletonization using napari
The python script [Visualize_Segment_Skeleton.py](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Visualize_Segment_Skeleton.py) permits visualization of the outputs of segmenting the fibers, followed by skeletonization. These are crucial steps for the downstream `quanfima` analysis.  
First, images are loaded using `dask-image` with each image being a block in a dask array. Then segmentation and skeletonization steps are applied using `map_blocks`, a `dask.array` method that applies a function to an array (here stack of images) block-wise (here image by image).  
Using napari these steps can be visualized lazily, on a per-image basis, without pre-computing for every image. The computations are performed when a slice is selected.

[^1]: Note: In python3, the `quanfima` module has some problems due to relatively old dependencies. A fork capable of running 2D image fiber analysis in python3 is available: [https://github.com/psobolewskiPhD/quanfima](https://github.com/psobolewskiPhD/quanfima)
