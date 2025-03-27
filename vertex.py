import argparse


# ----------------------------------------------------------------------------# 
# ------------------          Argument Processing           ------------------# 
# ----------------------------------------------------------------------------# 


def check_arguments(args):
    """ """
    return args


def process_arguments(test_args: list = None):
    """ Argument processing arguments"""

    parser = argparse.ArgumentParser(prog='VERTEX',
                                     description='Accelerated vertex functional connectivity toolkit')

    MODES = ["fc-sparse", "all"]

    # General Arguments
    parser.add_argument('-s', "--seed", dest='seed', action="store", type=int, default=137,
                        required=False, help="Random seed")
    parser.add_argument("-m", '--mode', choices=MODES, type=str, default="all",
                        help=f'Precision mapping options: {MODES}')

    args = parser.parse_args() if test_args is None else parser.parse_args(test_args)
    return check_arguments(args)


# ----------------------------------------------------------------------------# 
# --------------------                Main                --------------------# 
# ----------------------------------------------------------------------------# 


def main():
    """ """
    args = process_arguments()


if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
