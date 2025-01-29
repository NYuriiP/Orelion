import sqlite3
import json


class GamePersistence:

  def __init__(self, dbName="game.db"):
    self.db = sqlite3.connect(dbName)
    self.cursor = self.db.cursor()
    res = self.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='game_saves'"
    )
    if res.fetchone() is None:
      self.initSchema()

  def initSchema(self):
    self.cursor.execute(
        "CREATE TABLE game_saves(id INTEGER PRIMARY KEY, name TEXT NOT NULL, data TEXT, date_created TEXT NOT NULL)"
    )
    # other tables like rooms, items, can be initialised here

  def saveGame(self, name, game_data):
    self.cursor.execute(
        "SELECT id FROM game_saves WHERE name=?", (name,))
    existing_id = self.cursor.fetchone()
    if existing_id:
      self.cursor.execute(
          "UPDATE game_saves SET data=?, date_created=datetime('now') WHERE id=?",
          (json.dumps(game_data, default=vars), existing_id[0]))
    else:
      self.cursor.execute(
          "INSERT INTO game_saves(name, data, date_created) VALUES(?, ?, datetime('now'))",
          (name, json.dumps(game_data, default=vars)))
    self.db.commit()

  def loadGame(self, save_name):
    self.cursor.execute("SELECT data FROM game_saves WHERE name=?",
                        (save_name, ))
    data = self.cursor.fetchone()
    if data is None:
      return None
    return json.loads(data[0])

  def deleteGame(self, id):
    self.cursor.execute("DELETE FROM game_saves WHERE id=?", (id, ))
    self.db.commit()

  def getGameIds(self):
    self.cursor.execute("SELECT id, name FROM game_saves")
    return [(row[0], row[1]) for row in self.cursor.fetchall()]
