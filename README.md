This repository has the code for the bacterial cellulose fiber analysis (using SEM) that has been published as:  
"Silicone polyether surfactant enhances bacterial cellulose synthesis and water holding capacity"  
International Journal of Biological Macromolecules, 2022  
https://doi.org/10.1016/j.ijbiomac.2022.03.124

# SEM_fiber_analysis
This repository contains python scipts to perform fiber analysis in SEM images.
It uses [scikit-image](https://github.com/scikit-image/scikit-image) and [quanfima](https://github.com/rshkarin/quanfima)[^1] for the analysis, [dask](https://github.com/dask/dask) for lazy-loading and parallelization, and [napari](https://github.com/napari/napari) for intermediate outcome visualization.

# Step-by-step example workflow
The Jupyter notebook [`Example_Fiber_analysis.ipynb`](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Example_Fiber_analysis.ipynb) provides a step-by-step example of the image analysis workflow, using a representative SEM of bacterial cellulose fibers, provided in the [`fiber_data` folder](https://github.com/psobolewskiPhD/SEM_fiber_analysis/tree/main/fiber_data). An exported [PDF version](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Example_Fiber_analysis.pdf) is also provided.

# Visualizing the segmentation and skeletonization using napari
The python script [Visualize_Segment_Skeleton.py](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Visualize_Segment_Skeleton.py) permits visualization of the outputs of segmenting the fibers, followed by skeletonization. These are crucial steps for the downstream `quanfima` analysis.  
First, images are loaded using `dask-image` with each image being a block in a dask array. Then segmentation and skeletonization steps are applied using `map_blocks`, a `dask.array` method that applies a function to an array (here stack of images) block-wise (here image by image).  
Using napari these steps can be visualized lazily, on a per-image basis, without pre-computing for every image. The computations are performed when a slice is selected.

# Computing the fiber properties (porosity, orientations, and diameters) using `quanfima`
The python script [Analyze_fibers.py](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Analyze_fibers.py) calculates the fiber parameters using `quanfima` `morphology` module.  
As previously, images are loaded using `dask-image` with each image being a block in a dask array. Then segmentation is obtained using `map_blocks`, as previously described.    
Next, a function is defined to calculate the porosity using `quanfima` and the calculation is parallelized using `dask`. The outputs are paired up with the names of the input images and returned as a dict.   
Finally, the segmented images are used to obtain the fiber orientations and diameters again using `quanfima`. As previously, the calculation is parallelized using `dask`.  
*Note: it can take ~1 min per image to run this, so it's recommended to consider using the `processess` scheduler or the `dask.distributed` scheduler. See [the Dask scheduler docs](https://docs.dask.org/en/latest/scheduler-overview.html) for details.*  
Summary values (means and standard deviations) are computed, paired up with the input images names, and returned as a dict.

[^1]: Note: In python3, the `quanfima` module has some problems due to relatively old dependencies. A fork capable of running 2D image fiber analysis in python3 is available: [https://github.com/psobolewskiPhD/quanfima](https://github.com/psobolewskiPhD/quanfima)
