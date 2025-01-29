from gamePersistence import GamePersistence
persistance = GamePersistence()
def save_player_data(player):
    """Saves the player's data to SQLite."""
    player_data = {
        "name": player.name,
        "sex": player.sex,
        "origin": player.origin,
        "age": player.age,
        "DEF": player.DEF,
        "SPD": player.SPD,
        "ATK": player.ATK,
        "MAXHP": player.MAXHP,
        "MAXMANA": player.MAXMANA,
        "KARMA": player.KARMA,
        "inventory": player.inventory,
        "headSlot": player.headSlot,
        "bodySlot": player.bodySlot,
        "legSlot": player.legSlot,
        "accessorySlot": player.accessorySlot,
        "weaponEquipped": player.weaponEquipped,
        "current_location": player.current_location
    }
    persistance.saveGame(player.name, player_data)
def load_player_data(save_name):
    """Loads the player's data from SQLite."""
    try:
        player_data = persistance.loadGame(save_name)
        return player_data
    except Exception as e:
        print(f"Error loading save file {save_name}: {e}")
        return None

def save_game(player):
    print("Saving the game...")
    save_player_data(player)

def continue_game():
    print("Continuing the game...")

def quit_game():
    print("Quitting the game...")
    exit()
