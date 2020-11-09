from collections import Iterable
import re


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


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,4})\d*$',r'\1', str(num)))


def dried(ingredient, moisture):
    percent = (ingredient / (100 - moisture)) * 100
    return truncate(percent)
