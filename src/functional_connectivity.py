import nibabel as nb
import numpy as np
import scipy

import torch

from . import correlators as corr
from . import utils

# ----------------------------------------------------------------------------# 
# --------               Functional Connectivity Tools                --------# 
# ----------------------------------------------------------------------------# 


def calculate_vertex_FC(cifti_path, save_path=None, sparsity=0.1,
                        exclude_index_path=None, mask_path=None,
                        block_size=5000, leave=True, device="auto", **SC_kwargs):
    """ """
    device = utils.get_device(device)
    print(device)
    exclude_index = np.load(exclude_index_path) if exclude_index_path else None 
    mask = scipy.sparse.load_npz(mask_path) if mask_path else None


    cifti = nb.load(cifti_path)
    vertex_data = cifti.get_fdata(caching="unchanged")

    sc = corr.SparseCorrelator.run(vertex_data, sparsity_percent=sparsity,
                                   mask=mask, exclude_index=exclude_index,
                                   symmetric=True, block_size=block_size, leave=leave,
                                   device=device,
                                   **SC_kwargs)
    if save_path:
        scipy.sparse.save_npz(save_path, sc)

    return sc



def correlate_vertex_FC(cifti_path, cifti_2_path, save_path=None, threshold=None,
                        exclude_index_path=None, mask_path=None,
                        block_size=1_000, leave=True, device="auto", **SC_kwargs):
    """ """
    device = utils.get_device(device)

    exclude_index = np.load(exclude_index_path) if exclude_index_path else None 
    mask = scipy.sparse.load_npz(mask_path) if mask_path else None


    cifti = nb.load(cifti_path)
    # TODO: REMOVE CROP
    vertex_data = cifti.get_fdata(caching="unchanged")[:, :]

    cifti_2 = nb.load(cifti_2_path)
    vertex_data_2 = cifti_2.get_fdata(caching="unchanged")[:, :]

    pair_data = np.stack((vertex_data, vertex_data_2), axis=2)
    r_axis = corr.pair_correlation(pair_data, axis=0, threshold=threshold,
                              mask=None, exclude_index=None, leave=True,
                              block_size=5000, symmetric=False,
                              backend="torch", device=device, **SC_kwargs)
    
    # TODO save r_axis as dscalar
    if save_path:
        np.save(save_path, r_axis)

    return r_axis

# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
