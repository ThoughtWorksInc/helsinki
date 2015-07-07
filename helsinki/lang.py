import yaml
import string
from pkg_resources import resource_string


# if there is a key collision then dict2 will be favoured
def merge_dicts(dict1, dict2):
    d1 = dict1.copy()
    for k in dict2:
        v1 = dict1.get(k)
        v2 = dict2.get(k)
        if isinstance(v1, dict):
            d1[k] = merge_dicts(v1, v2)
        else:
            d1[k] = v2
    return d1


en = yaml.load(resource_string(__name__, 'language/en.yml'))
fi = merge_dicts(en, yaml.load(resource_string(__name__, 'language/fi.yml')))


def load_translation_data_for_code(code):
    if code.lower() == "fi":
        return fi
    else:
        return en


def load_translation(lang, p):
    path = string.split(p.lower(), '.')
    data = load_translation_data_for_code(lang)
    for part in path:
        data = data.get(part)
        if data is None:
            return "MISSING TRANSLATION"
    if data:
        return data
    else:
        return "MISSING TRANSLATION"


def translator(lang):
    return lambda p: load_translation(lang, p)


def _translate_result(lang, result):
    result["friendly_day"] = load_translation(lang, "dates.%s" % result["friendly_day"])
    return result


def translate_results(lang, results):
    return [_translate_result(lang, result) for result in results]
