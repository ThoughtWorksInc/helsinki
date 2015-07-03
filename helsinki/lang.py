import yaml
import string
from pkg_resources import resource_string

en = yaml.load(resource_string(__name__, 'lang.yml'))


def load_translation(p):
    path = string.split(p, '.')
    data = en
    for part in path:
        data = data.get(part)
        if data is None:
            return "MISSING TRANSLATION"
    if data:
        return data
    else:
        return "MISSING TRANSLATION"
