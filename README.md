[![PyPI version](https://badge.fury.io/py/vertex-FC.svg)](https://pypi.org/project/vertex-FC/)
[![License](https://img.shields.io/pypi/l/vertex-FC)](https://pypi.org/project/vertex-FC/)

# VERTEX-FC: Accelerated fMRI Functional Connectivity Tools
VERTEX-FC is a a python for functional connectivity analysis at the voxel / vertex level that utilizes pytorch for GPU speed ups and scipy sparse matrices for memory savings.

# Tools:
	[] list tools: vFC tools
		- Efficient creation of sparse vertex level FC matrices
		- Efficient comparisons between vertex level FC matrices

	[] clustering methods:
		[] PM: infomaps - for individual parcellations
		[] PM: with other clustering techniques
		[] PM: integrate with Sparse-Low Rank Clustering

# Installation and Usage

Install from PyPI:

```pip install vertex-FC```

Example Usage:
```python vertex -m comapre -c cifti1.dtseries.nii -c2 cifti2.dtseries.nii -o output_cifti.dscalar.nii```

Can able be imported as a package:

```
import vertex
vFC_matrix = vertex.calculate_vertex_FC(cifti_data, sparsity=0.1)
```

# Acceleration Effects:
Comparisons are with `wb_command` package (~~version~~):


## Time Speed Up
	[] Creating dconns:
	[] Creating sparse dconns:
	[] Dconn comparisons

## Memory Savings
	[] Creating dconns
	[] Sparse dconns
	[] Dconn comparisons

## Storage Savings
	[] Sparse dconns
	[] Dconn comparisons


# TODO:
	[] plots: no surface plotting features (too messy)
	[] benchmarking
		[] create time benchmark plots for devices
		[] benchmark script:
			[x] runs on machine: records time of set functions
			[] outputs: json with memory over time, time to run each function, device info
			[] plots: have bar chart with resource (time, memory, etc) improvement plot by task and device:
				- ex.  y axis time, x axis is task, hue is device (M1, M2, M2 Ultra, RTX3080/3090)
	[] main:
		[x] vFC corr
			[x] sparse is working
			[] implement threshold:
				[] argument that specifies sparsity or threshold and then respective func is used
				[] arg checks (sparse values < 10%, threshold > 0.05 -> unlikely to be sparse?)
		[] vFC compare:
			[x] main compare works
			[] write r axis to cifti
			[] write single r value to ***???
				[] r single is also only approximate now!! would need to turn into real

			[] option to compare many ciftis?
				- doesnt really make sense for axis, besides preloading into memory (marginal speed up?)
				- 
		[] kernel smoothing:
			[] likely requires gifti neighbor map - only one and could store as resource?
				[] or just save neighbors into resource pkl
			[] for neighbor hood value, is weighted average of neighbors (weight is function of distance)
			[] applied immediately after loading cifti in

