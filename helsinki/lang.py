import yaml
import string

f = open('lang.yml')

en = yaml.load(f.read())

f.close()


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
