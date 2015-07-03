import yaml
import string
from pkg_resources import resource_string

en = yaml.load(resource_string(__name__, 'lang.yml'))


def load_translation(p):
    path = string.split(p.lower(), '.')
    data = en
    for part in path:
        data = data.get(part)
        if data is None:
            return "MISSING TRANSLATION"
    if data:
        return data
    else:
        return "MISSING TRANSLATION"


def _translate_result(result):
    result["friendly_day"] = load_translation("dates.%s" % result["friendly_day"])
    return result


def translate_results(results):
    return [_translate_result(result) for result in results]
