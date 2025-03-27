import argparse
import os

from src import utils
from src import functional_connectivity as FC

vertex_dir = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.join(vertex_dir, "../")

# ----------------------------------------------------------------------------# 
# ------------------          Argument Processing           ------------------# 
# ----------------------------------------------------------------------------# 


def check_arguments(args):
    """ """

    if args.mode == "comapre":
        assert args.cifti_2 is not None


    assert os.path.exists(args.cifti)
    save_dir = os.path.dirname(args.save_path)
    if save_dir != "":
        assert os.path.exists(save_dir)

    return args


def process_arguments(test_args: list = None):
    """ Argument processing arguments"""

    parser = argparse.ArgumentParser(prog='VERTEX',
                                     description='Accelerated vertex functional connectivity toolkit')

    MODES = ["sparse", "compare"]

    # General Arguments
    parser.add_argument('-s', "--seed", dest='seed', action="store", type=int, default=137,
                        required=False, help="Random seed")
    parser.add_argument("-m", '--mode', choices=MODES, type=str, default="sparse",
                        help=f'vertex options: {MODES}')

    parser.add_argument('-c', "--cifti", dest='cifti', action="store", type=str, required=True, help="path to cifti")
    parser.add_argument('-c2', "--cifti-2", dest='cifti_2', action="store", type=str,
                        required=False, help="path to cifti 2 for comparisons")
    parser.add_argument('-o', "--out", dest='save_path', action="store", type=str, required=True, help="save path")
    

    args = parser.parse_args() if test_args is None else parser.parse_args(test_args)
    return check_arguments(args)


# ----------------------------------------------------------------------------# 
# --------------------                Main                --------------------# 
# ----------------------------------------------------------------------------# 


def main(test_args: list = None):
    """ """
    args = process_arguments(test_args=test_args)

    if args.mode == "sparse":
        FC.calculate_vertex_FC(args.cifti, args.save_path, sparsity=0.1,
                        exclude_index_path=None, mask_path=None,
                        block_size=5000, leave=True)

        raise NotImplementedError
    elif args.mode == "compare":
        raise NotImplementedError


if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
