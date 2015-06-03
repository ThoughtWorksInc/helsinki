import json

import requests


class APIError(Exception):
  pass


def import_decision_data():
  r = requests.get('http://dev.hel.fi/paatokset/v1/issue/')
  if r.status_code not in [200, 201]:
    raise APIError()
  
  return r.json()

