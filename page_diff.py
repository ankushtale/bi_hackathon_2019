from PyPDF2 import PdfFileReader
import os
from utils import unique_values_in_list, are_all_elements_in_list_equal


def get_page_count(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()

    return number_of_pages


def get_page_number_diffs(files_to_read):
    page_diff = dict()

    dict_files_and_pages = get_pages(files_to_read)

    file_prefixes = [file_prefix.split("_")[0] for file_prefix in dict_files_and_pages]

    unique_file_prefixes = unique_values_in_list(file_prefixes)

    for unique_file_prefix in unique_file_prefixes:
        unique_file_prefix_page_numbers = [v for k, v in dict_files_and_pages.items()
                                           if k.startswith(unique_file_prefix)]
        corresponding_file_names = [k for k, v in dict_files_and_pages.items()
                                    if k.startswith(unique_file_prefix)]
        if len(unique_file_prefix_page_numbers) == 1:
            page_diff[corresponding_file_names[0]] = unique_file_prefix_page_numbers[0]
        elif are_all_elements_in_list_equal(unique_file_prefix_page_numbers):
            for file in corresponding_file_names:
                page_diff[file] = True
                # page_diff[unique_file_prefix] = False
        else:
            for file in corresponding_file_names:
                page_diff[file] = False
            # page_diff[unique_file_prefix] = False

    return page_diff


def get_pages(files_to_read):
    dict_files_and_pages = dict()

    if len(files_to_read) == 0:
        return False

    for file in files_to_read:
        dict_files_and_pages[os.path.basename(file)] = get_page_count(file)

    return dict_files_and_pages
