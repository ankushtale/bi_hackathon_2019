import argparse


def parse_args():
    """
    Parses the argument list to main
    :return: Dictionary of all arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--source_dir", nargs='?', help="Provide location where all documents are stored", default=None)

    parsed_args_dict = vars(parser.parse_args())

    return parsed_args_dict
