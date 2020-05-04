from typing import Iterable


def print_pair(key, value):
    if key is None:
        print(value)
    else:
        print(f"{key}: {value}")


def printout(item, key = None):
    try:
        if isinstance(item, set):
            print_pair(key, item)
        elif isinstance(item, Iterable):
            for sub_item in item:
                printout(item[sub_item], sub_item)
        else:
            print_pair(key, item)
    except:
        print_pair(key, item)
