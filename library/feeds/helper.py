from collections import Iterable


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


def search_id(match, data):
    """
    list içerisindeki elemanlarda id araması için
    eğer varsa elemanı döndürür
    """
    return [element for element in data if element['id'] == match]
