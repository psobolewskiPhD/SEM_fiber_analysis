# SEM_fiber_analysis
This repository contains python scipts to perform fiber analysis in SEM images.
It uses [scikit-image](https://github.com/scikit-image/scikit-image) and [quanfima](https://github.com/rshkarin/quanfima)[^1] for the analysis, [dask](https://github.com/dask/dask) for lazy-loading and parallelization, and [napari](https://github.com/napari/napari) for intermediate outcome visualization.
A Jupyter notebook provides a step-by-step example of the image analysis workflow, using a representative SEM of bacterial cellulose fibers.

[^1]: Note: In python3, the `quanfima` module has some problems due to relatively old dependencies. A fork capable of running 2D image fiber analysis in python3 is available: [https://github.com/psobolewskiPhD/quanfima](https://github.com/psobolewskiPhD/quanfima)
