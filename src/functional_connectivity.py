import nibabel as nb
import numpy as np
import scipy

from . import correlators as corr

# ----------------------------------------------------------------------------# 
# --------               Functional Connectivity Tools                --------# 
# ----------------------------------------------------------------------------# 


def calculate_vertex_FC(cifti_path, save_path=None, sparsity=0.1,
                        exclude_index_path=None, mask_path=None,
                        block_size=5000, leave=True, **SC_kwargs):
    """ """
    exclude_index = np.load(exclude_index_path) if exclude_index_path else None 
    mask = scipy.sparse.load_npz(mask_path) if mask_path else None


    cifti = nb.load(cifti_path)
    vertex_data = cifti.get_fdata(caching="unchanged")

    sc = corr.SparseCorrelator.run(vertex_data, sparsity_percent=sparsity,
                                   mask=mask, exclude_index=exclude_index,
                                   symmetric=True, block_size=block_size, leave=leave,
                                   **SC_kwargs)
    if save_path:
        scipy.sparse.save_npz(save_path, sc)

    return sc


# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
