import collections

def flatten(l):
    """
    配列のを１次元にする
    """
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el
            

def remove_empty_from_array(arr: list) -> list:
    """
    remove empty from list
    ex) ['a', 'b', '', 'c'] -> ['a', 'b', 'c']
    """
    return list(filter(None, arr))