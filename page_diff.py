from PyPDF2 import PdfFileReader
import os


def are_all_elements_in_list_equal(lst):
    return lst[1:] == lst[:-1]


def unique_values_in_list(l):
    list_set = set(l)
    # convert the set to the list
    return list(list_set)


def listdir_full_path(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def get_page_count(path):

    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()

    return number_of_pages


def get_page_number_diffs(files_to_read):

    dict_files_and_pages = dict()
    page_diff = dict()

    if len(files_to_read) == 0:
        return False

    for file in files_to_read:
        dict_files_and_pages[os.path.basename(file)] = get_page_count(file)
        # print("File: {} #Pages: {}".format(os.path.basename(file), get_page_count(file)))

    file_prefixes = [file_prefix.split("_")[0] for file_prefix in dict_files_and_pages]

    unique_file_prefixes = unique_values_in_list(file_prefixes)

    for unique_file_prefix in unique_file_prefixes:
        unique_file_prefix_page_numbers = [v for k, v in dict_files_and_pages.items() if k.startswith(unique_file_prefix)]
        if len(unique_file_prefix_page_numbers) == 1:
            page_diff[unique_file_prefix] = unique_file_prefix_page_numbers[0]
        elif are_all_elements_in_list_equal(unique_file_prefix_page_numbers):
            page_diff[unique_file_prefix] = True
        else:
            page_diff[unique_file_prefix] = False

    return page_diff