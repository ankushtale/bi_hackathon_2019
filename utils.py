import os


def unique_values_in_list(l: list) -> list:
    list_set = set(l)
    # convert the set to the list
    return list(list_set)


def are_all_elements_in_list_equal(lst):
    return lst[1:] == lst[:-1]


def listdir_full_path(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


