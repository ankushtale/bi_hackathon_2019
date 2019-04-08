import os


def is_markup_present(files_to_read):

    is_markup_present_flag = dict()

    for file in files_to_read:
        is_markup_present_flag[os.path.basename(file)] = False

    return is_markup_present_flag
