import os
import json
da_dict = {}


class db:
  @staticmethod
  def _set(file):
    da_dict['file'] = file
    return True

  @staticmethod
  def _append(key, val):
    with open(da_dict['file'], "r") as E:
      lE = json.load(E)
      lE[key] = val
    with open(da_dict['file'], "w") as E:
      json.dump(lE, E)
  
  @staticmethod
  def _unappend(key=None, mode='key'):
      with open(da_dict['file'], "r") as E:
        lE = json.load(E)
        if mode == "file":
          return dict(lE)

      with open(da_dict['file'], "r") as E:
        lE = json.load(E)
        return dict(lE)

class db_ext:
  @staticmethod
  def render(amount : list):
    with open(da_dict['file'], "r") as E:
      lE = json.load(E)
      for i in amount:
        yield lE[i]