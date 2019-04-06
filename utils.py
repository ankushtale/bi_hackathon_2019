import os
import pprint
import annotations
import page_diff


def listdir_full_path(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def julie_do_the_thing(src_dir):

    files_to_read = listdir_full_path(src_dir)

    files_to_read = [file for file in files_to_read if file.endswith('.pdf')]

    files_to_read.sort()

    print("***********Page Diffs***********")
    pprint.pprint(page_diff.get_page_number_diffs(files_to_read))

    print('____________________________________________')
    print("***********Annotations***********")
    pprint.pprint(annotations.are_annotations_present(files_to_read))




