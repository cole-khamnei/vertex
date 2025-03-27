import os
import sys

import numpy as np
import scipy

from concurrent.futures import ThreadPoolExecutor
from tqdm.auto import tqdm

from . import constants
from . import utils
from . 

# ----------------------------------------------------------------------------# 
# --------               Functional Connectivity Tools                --------# 
# ----------------------------------------------------------------------------# 


def generate_voxel_FC(voxel_data, save_path=None, sparsity=0.1, exclude_index_path=None,
                      mask_path=None, block_size=5000, leave=True, **SC_kwargs):
    """ """
    exclude_index = np.load(exclude_index_path) if exclude_index_path else None 
    mask = scipy.sparse.load_npz(mask_path) if mask_path else None

    sc = vtx.SparseCorrelator.run(voxel_data[:, :], mask=mask, symmetric=True, exclude_index=exclude_index,
                                  sparsity_percent=sparsity, block_size=block_size, leave=leave, **SC_kwargs)
    if save_path:
        scipy.sparse.save_npz(save_path, sc)

    return sc


# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
