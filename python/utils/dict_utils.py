#!/usr/bin/env python

import sys


def get_value_list(d):
    assert isinstance(d, dict)
    if sys.version_info[0] == 2:
        item_list = d.values()
    elif sys.version_info[0] == 3:
        item_list = list(d.values())
    else:
        # should not happen
        raise RuntimeError("Only python 2 and 3 supported.")
    assert isinstance(item_list, list)
    return item_list


def get_item_iterator(d):
    assert isinstance(d, dict)
    if sys.version_info[0] == 2:
        item_iter = d.iteritems()
        assert hasattr(item_iter, "next")
    elif sys.version_info[0] == 3:
        item_iter = iter(d.items())
        assert hasattr(item_iter, "__next__")
    else:
        # should not happen
        raise RuntimeError("Only python 2 and 3 supported.")
    assert hasattr(item_iter, "__iter__")
    return item_iter
