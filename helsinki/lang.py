import yaml
import string
from pkg_resources import resource_string

en = yaml.load(resource_string(__name__, 'language/en.yml'))
fi = yaml.load(resource_string(__name__, 'language/fi.yml'))


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
