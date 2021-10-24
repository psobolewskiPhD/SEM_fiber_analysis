# SEM_fiber_analysis
This repository contains python scipts to perform fiber analysis in SEM images.
It uses [scikit-image](https://github.com/scikit-image/scikit-image) and [quanfima](https://github.com/rshkarin/quanfima)[^1] for the analysis, [dask](https://github.com/dask/dask) for lazy-loading and parallelization, and [napari](https://github.com/napari/napari) for intermediate outcome visualization.

# Step-by-step example workflow
The Jupyter notebook [`Example_Fiber_analysis.ipynb`](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Example_Fiber_analysis.ipynb) provides a step-by-step example of the image analysis workflow, using a representative SEM of bacterial cellulose fibers, provided in the [`fiber_data` folder](https://github.com/psobolewskiPhD/SEM_fiber_analysis/tree/main/fiber_data). An exported [PDF version](https://github.com/psobolewskiPhD/SEM_fiber_analysis/blob/main/Example_Fiber_analysis.pdf) is also provided.

[^1]: Note: In python3, the `quanfima` module has some problems due to relatively old dependencies. A fork capable of running 2D image fiber analysis in python3 is available: [https://github.com/psobolewskiPhD/quanfima](https://github.com/psobolewskiPhD/quanfima)
