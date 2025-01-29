from saveSystem import save_player_data, quit_game
from lbl import lbl
from getResponse import getResponse
def RogueSpawn():
  global choices
  with open("Liuria", "r") as file:
    lines = file.readlines()
  for i in range(3, 9):
    line = lines[i]
    text = line[line.index("RogueSpawnText") + len("RogueSpawnText") + 4]
    lbl(text + "\n", "clear", 0.03, "")
  print("\n")
  choices = [
      "Move towards the city.", "Move away from the city.",
      "Move towards the forest.", "Move towards the outpost.", "Check status.",
      "Check inventory.", "save", "quit"
  ]
  choice = getResponse("what would you like to do? ", choices)
  while player.current_location == "RogueSpawn":
    match choice:
      case 1:
        player.current_location = "LiuriaCityGate"
      case 2:
        player.current_location = "FrozenWilds1"
      case 3:
        player.current_location = "LiuriaForest"
      case 4:
        player.current_location = "LiuriaOutpost1"
      case 5:
        player.status()
      case 6:
        player.checkInventory()
      case 7:
        save_player_data(player)
      case 8:
        quit_game()
    choice = get_response("what would you like to do? ", choices)
