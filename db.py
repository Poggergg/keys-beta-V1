import os
import json
Udb = {}
Mdb = {}

class userDB:
  """Database(JSON) to handle User creation"""
  @staticmethod
  def _set(file):
    """Setting the file used for User Database"""
    Udb['file'] = file
    return True

  @staticmethod
  def _append(key, val):
    """Appends the user to a JSON file with the scopes"""
    with open(Udb['file'], "r") as E:
      lE = json.load(E)
      lE[key] = val
    with open(Udb['file'], "w") as E:
      json.dump(lE, E)
  
  @staticmethod
  def _unappend(key=None, mode='key'):
    """Unappends the user to handle :name:, :password:, :ID:, :etc:"""
    with open(Udb['file'], "r") as E:
      lE = json.load(E)
      if mode == "file":
        return dict(lE)

    with open(Udb['file'], "r") as E:
      lE = json.load(E)
      return dict(lE)

class msgDB:
  @staticmethod
  def _set(db):
    Mdb['file'] = db
    return True

  @staticmethod
  def _append(message, append_id):
    with open(Mdb['file'], 'r') as P:
      lP = json.load(P)
      lP[append_id] = message
    with open(Mdb['file'], "w") as P:
      json.dump(lP, P)
      return message
  
  @staticmethod
  def _unappend(append_id):
    with open(msgDB.mdb, 'r') as P:
      lP = json.load(P)
      try:
        return lP[append_id]
      except KeyError:
        return "404 message not found"
  
      

class db_ext:
  @staticmethod
  def render(amount : list):
    with open(Udb['file'], "r") as E:
      lE = json.load(E)
      for i in amount:
        yield lE[i]