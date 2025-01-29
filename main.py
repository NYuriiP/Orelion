# ──────────────────────────────────────────────────────────────────────
# ────────────────────────────── libraries ─────────────────────────────
# ──────────────────────────────────────────────────────────────────────

import os
from map import game_map
from lbl import lbl, TEXT_SPEED
from saveSystem import save_player_data, load_player_data
from gamePersistence import GamePersistence
import RogueSpawn as RS
from getResponse import getResponse

# ──────────────────────────────────────────────────────────────────────
# ───────────── variables, constants, lists & dictionaries ─────────────
# ──────────────────────────────────────────────────────────────────────

persistance = GamePersistence()
choices = []

# ──────────────────────────────────────────────────────────────────────
# ────────────────────────────── classes ───────────────────────────────
# ──────────────────────────────────────────────────────────────────────


class Area:

  def __init__(self, description, encounter_pool, items_collected=[]):
    self.description = description
    self.encounter_pool = encounter_pool
    self.items_collected = items_collected


class Entity:

  def __init__(self, name, sex, origin, age, DEF, SPD, ATK, MAXHP, MAXMANA):
    self.name = name  # assigned in void
    self.sex = sex  # assigned in void
    self.age = age  # assigned in void
    self.origin = origin  # assigned in void
    self.HP = 100  # temporary value, might change later
    self.MAXHP = 100  # temporary value, might change later
    self.MANA = 100  # temporary value, might change later
    self.MAXMANA = 100  # temporary value, might change later
    self.ATK = ATK  # assigned in void
    self.SPD = SPD  # assigned in void
    self.DEF = DEF  # assigned in void

  def attack(self, target):
    damage = self.ATK - target.DEF
    target.HP -= (damage, 0)
    print(f"{self.name} attacks {target.name} for {damage} damage!")

  def defend(self, attack):
    damage = attack - self.DEF
    if damage < 0:
      damage = 0
    self.HP -= damage
    print(
        f"{self.name} defends against {attack} damage and takes {damage} damage."
    )

  def heal(self, amount):
    self.HP += amount
    if self.HP > self.MAXHP:
      self.HP = self.MAXHP
    print(f"{self.name} heals for {amount} HP.")


class Player(Entity):

  def __init__(self, name, sex, origin, age, DEF, SPD, ATK, MAXHP, MAXMANA,
               KARMA):
    super().__init__(name, sex, origin, age, DEF, SPD, ATK, MAXHP, MAXMANA)
    self.headSlot = ["", ""]  # standard
    self.bodySlot = ["Old Tunic", ""]  # standard
    self.legSlot = ["Old Trousers", ""]  # standard
    self.accessorySlot = ["silver ring", ""]  # standard
    self.weaponEquipped = ["Travellers blade", ""]  # assigned in void
    self.KARMA = 0  # assigned in void
    self.inventory = []
    self.current_location = "void"

  def checkInventory(self):
    for i in self.inventory:
      print(f"- {i}")

  def checkEquipped(self):
    print(f"- Weapon Equipped: {self.weaponEquipped[0]}")
    print(f"- Head Equipped: {self.headSlot[0]}")
    print(f"- Body Equipped: {self.bodySlot[0]}")
    print(f"- Leg Equipped: {self.legSlot[0]}")
    print(f"- Accessory Equipped: {self.accessorySlot[0]}")

  def equipWeapon(self, weapon):
    if weapon in self.inventory:
      self.weaponEquipped = weapon
      self.inventory.remove(weapon)
      print(f"{weapon} equipped.")
    else:
      print(f"You do not have {weapon} in your inventory.")

  def equipHead(self, item):
    if item in self.inventory:
      self.headSlot[0] = item
      self.inventory.remove(item)
      print(f"{item} equipped.")
    else:
      print(f"You do not have {item} in your inventory.")

  def equipBody(self, item):
    if item in self.inventory:
      self.bodySlot[0] = item
      self.inventory.remove(item)
      print(f"{item} equipped.")
    else:
      print(f"You do not have {item} in your inventory.")

  def equipLegs(self, item):
    if item in self.inventory:
      self.legSlot[0] = item
      self.inventory.remove(item)
      print(f"{item} equipped.")
    else:
      print(f"You do not have {item} in your inventory.")

  def equipAmulet(self, item):
    if item in self.inventory:
      self.accessorySlot[0] = item
      self.inventory.remove(item)
      print(f"{item} equipped.")
    else:
      print(f"You do not have {item} in your inventory.")

  def unequipWeapon(self):
    if self.weaponEquipped != "":
      self.inventory.append(self.weaponEquipped)
      self.weaponEquipped = ""
      print("Weapon unequipped.")
    else:
      print("No weapon is currently equipped.")

  def unequipHead(self):
    if self.headSlot[0] != "":
      self.inventory.append(self.headSlot[0])
      self.headSlot[0] = ""
      print("Headgear unequipped.")
    else:
      print("No headgear is currently equipped.")

  def unequipBody(self):
    if self.bodySlot[0] != "":
      self.inventory.append(self.bodySlot[0])
      self.bodySlot[0] = ""
      print("Body armor unequipped.")
    else:
      print("No body armor is currently equipped.")

  def unequipLegs(self):
    if self.legSlot[0] != "":
      self.inventory.append(self.legSlot[0])
      self.legSlot[0] = ""
      print("Leg armor unequipped.")
    else:
      print("No leg armor is currently equipped.")

  def unequipAmulet(self):
    if self.accessorySlot[0] != "":
      self.inventory.append(self.accessorySlot[0])
      self.accessorySlot[0] = ""
      print("Amulet unequipped.")
    else:
      print("No amulet is currently equipped.")

  def addInventory(self, item):
    self.inventory.append(item)
    print(f"{item} added to inventory.")

  def removeInventory(self, item):
    if item in self.inventory:
      self.inventory.remove(item)
      print(f"{item} removed from inventory.")
    else:
      print(f"You do not have {item} in your inventory.")

  def status(self):
    print(f"\n{self.name}'s Status")
    print(f"HP: {self.HP}/{self.MAXHP}")
    print(f"ATK: {self.ATK}")
    print(f"SPD: {self.SPD}")
    print(f"DEF: {self.DEF}")
    print("Inventory:")
    self.checkInventory()
    print("Equipped:")
    self.checkEquipped()

  def movement(self):
    if self.current_location in game_map:
      for idx, area in enumerate(game_map[self.current_location]):
        lbl(f"{idx + 1} - {area} \n", "clear", TEXT_SPEED, "")
      print("\n")
      destination = input("where would you like to go? ")
      try:
        if (int(destination) > len(game_map[self.current_location])):
          raise ValueError()
      except ValueError:
        print("this is not a valid location. ")
        return self.movement()


class NPC(Entity):

  def __init__(self, name, sex, origin, age, DEF, SPD, ATK, MAXHP, MAXMANA,
               description, reputation):
    super().__init__(name, sex, origin, age, DEF, SPD, ATK, MAXHP, MAXMANA)
    self.description = description  # assigned on init
    self.reputation = reputation  # assigned on init

  def status(self):
    print(f"\n{self.name}'s Status")
    print(f"HP: {self.HP}/{self.MAXHP}")
    print(f"MANA: {self.MANA}/{self.MAXMANA}")
    print(f"Description: {self.description}")


# ──────────────────────────────────────────────────────────────────────
# ─────────────────────── functions & procedures ───────────────────────
# ──────────────────────────────────────────────────────────────────────


def playerChoice(choices):
  for i in range(len(choices)):
    lbl(f"{i+1} - {choices[i]}", "clear", TEXT_SPEED, "")
  print("\n")
  lbl("what do you do? ", "clear", TEXT_SPEED, "")
  while True:
    try:
      choice = int(input()) - 1
      if 0 <= choice < len(choices):
        return choice
      else:
        print("Invalid choice, please select a valid option.")
    except ValueError:
      print("Please enter a valid number.")





# ──────────────────────────────────────────────────────────────────────
# ─────────────────────────────── places ───────────────────────────────
# ──────────────────────────────────────────────────────────────────────


def void():
  choice = ""
  origin = ""
  dfc = 0
  atk = 0
  spd = 0
  hp = 0
  mna = 0
  mrl = 0
  name = ""
  sex = ""
  purpose = ""

  lbl(
      "You awaken in an endless expanse of darkness. The void stretches infinitely in every direction, a realm without form or substance. There is no ground beneath you, ",
      "clear", TEXT_SPEED, "")
  lbl("yet you stand", "yellow", 0.1, "")
  lbl(
      ".\nThere is no sky above, only a shifting, inky blackness dotted with faint, flickering lights, like stars too timid to shine.",
      "clear", TEXT_SPEED, "")
  print("\n\n")
  lbl(
      "In the center of this emptiness stands a mannequin, featureless and still. Its smooth, pale surface reflects the faint glimmers of the void, an empty vessel, ",
      "clear", TEXT_SPEED, "")
  lbl("awaiting definition", "yellow", 0.1, "")
  lbl(".", "clear", TEXT_SPEED, "")
  print("\n\n")
  lbl("...", "clear", 0.7, "")
  print("\n\n")
  lbl("a voice, calm and without origin, calls out to you.\n", "clear",
      TEXT_SPEED, "")
  lbl('"What is your name?"\n\n', "magenta", TEXT_SPEED, "")
  name = input()

  print("\n\n")
  sex = getResponse("What is your sex?", ["Male", "Female"])

  match sex:
    case "1":
      lbl(
          "The mannequin subtly transforms, its curves tightening into stronger angles. The shoulders broaden, and the chest expands with quiet strength. A more masculine form emerges—solid, poised, with a presence that feels grounded and resolute.",
          "yellow", TEXT_SPEED, "")
      sex = "Male"
    case "2":
      lbl(
          "The mannequin subtly shifts, its sharp angles softening into gentle curves. The broadness of its shoulders narrows, and the waist cinches gracefully. A quiet, feminine form emerges, balanced with a quiet strength and poise, as if carved from the void itself.",
          "yellow", TEXT_SPEED, "")
      sex = "Female"

  print("\n\n")
  choice = getResponse("Who are you?", [
      "I am a warrior, forged in battle.",
      "I am a seeker of knowledge, a scholar of the unknown.",
      "I am a shadow, unseen and unheard.",
      "I am a protector, a shield for the helpless.",
      "I am an outcast, a wanderer with no home.",
      "I am an artist, a creator of beauty in a broken world.",
      "I am nothing... yet."
  ])

  match choice:
    case "1":
      origin = "Born into a war-torn land, shaped by conflict."
      lbl(
          "A jagged gash appears across the mannequin's face, a scar of hard-fought battles.",
          "yellow", TEXT_SPEED, "")
      atk += 1
      dfc += 1
    case "2":
      origin = "Raised in the archives of a vast library or as an apprentice to a mysterious mentor."
      lbl(
          "The mannequin's head tilts slightly as if deep in thought, and faint etchings of arcane symbols glow across its surface.",
          "yellow", TEXT_SPEED, "")
      mna += 2
    case "3":
      origin = "Born in the alleys of a bustling city, surviving by wit and guile."
      lbl(
          "The mannequin's form becomes slender and its edges blur, as though it is melting into the darkness.",
          "yellow", TEXT_SPEED, "")
      spd += 1
      mna += 1
    case "4":
      origin = "A village guardian or a member of a sacred order."
      lbl(
          "The mannequin's stance becomes firm and unyielding, like an immovable fortress.",
          "yellow", TEXT_SPEED, "")
      dfc += 2
    case "5":
      origin = "Exiled from a forgotten place, seeking redemption or purpose."
      lbl(
          "The mannequin's surface becomes rough and weathered, as though marked by years of travel.",
          "yellow", TEXT_SPEED, "")
      dfc += 1
      hp += 1
    case "6":
      origin = "Raised in a city of culture or as a dreamer in a humble village."
      lbl(
          "Splashes of vibrant color begin to swirl across the mannequin’s surface, as if painted by an unseen hand.",
          "yellow", TEXT_SPEED, "")
      mna += 1
      spd += 1
    case "7":
      origin = "A blank slate, allowing for a fully player-defined backstory."
      lbl(
          "The mannequin remains blank and featureless, yet its surface ripples like liquid, suggesting infinite potential.",
          "yellow", TEXT_SPEED, "")
      hp += 1
      mna += 1

  print("\n\n")
  choice = getResponse(
      "What is your greatest fear?",
      ["Weakness.", "Ignorance.", "Solitude.", "Betrayal.", "Failure."])

  match choice:
    case "1":
      lbl(
          "The mannequin’s once smooth and solid surface begins to crack and crumble, as though it can no longer bear its own weight.",
          "yellow", TEXT_SPEED, "")
      atk += 1
    case "2":
      lbl("A shadow falls over the mannequin's head, obscuring it from view.",
          "yellow", TEXT_SPEED, "")
      mna += 1
    case "3":
      lbl(
          "The mannequin’s figure becomes slightly hunched, its arms wrapping around itself as though seeking comfort or protection.",
          "yellow", TEXT_SPEED, "")
      spd += 1
    case "4":
      lbl(
          "A jagged crack forms across the mannequin’s chest, as though its heart has been split in two, a gentle red pulse comes from the crack.",
          "yellow", TEXT_SPEED, "")
      dfc += 1
    case "5":
      lbl(
          "The mannequin's once sturdy stance falters, and one knee bends slightly, as though it is on the verge of collapse.",
          "yellow", TEXT_SPEED, "")
      hp += 1

  print("\n\n")
  choice = getResponse("What will you sarcrifice for your desires?", [
      "My Integrity.", "My Humanity.", "My Relationships.", "My Comfort.",
      "My Innocence."
  ])

  match choice:
    case "1":
      lbl(
          "The mannequin’s once-clear surface begins to distort, taking on a mottled, corrupted appearance. Its reflection warps into something unrecognizable in the void surrounding it.",
          "yellow", TEXT_SPEED, "")
      dfc -= 1
    case "2":
      lbl(
          "The mannequin’s features blur and fade, merging with cold, metallic or ethereal elements. It becomes more alien, its once-human form barely recognizable, as if it's shedding its soul for something darker.",
          "yellow", TEXT_SPEED, "")
      spd -= 1
      mrl -= 1
    case "3":
      lbl(
          "The mannequin’s hands reach out but then retract, as if pulling away from unseen bonds. A cold, distant aura radiates from it, and cracks appear where it once seemed whole.",
          "yellow", TEXT_SPEED, "")
      atk -= 1
    case "4":
      lbl(
          "The mannequin’s form becomes battle-worn and scarred, as though it has endured years of hardship. It seems stronger, yet its expression carries the weight of sacrifice.",
          "yellow", TEXT_SPEED, "")
      hp -= 1
    case "5":
      lbl(
          "The mannequin’s smooth, pale surface becomes marred with dark stains or symbols, like ink or shadow bleeding into it. Its once-innocent expression becomes more knowing, even predatory, as if a part of it has shifted into something darker.",
          "yellow", TEXT_SPEED, "")
      mna -= 1

  print("\n\n")
  choice = getResponse("What will you do when you can no longer move forward?", [
          "I will retreat into myself, finding solace in solitude and reflection.",
          "I will burn everything down, destroying the obstacle and rebuilding from the ashes.",
          "I will search for another path, no matter how long it takes.",
          "I will accept my fate, letting go of the need to control anything.",
          "I will fight, even if there’s no chance of winning, just to prove I exist."
      ])

  match choice:
    case "1":
      lbl(
          "The mannequin’s posture subtly shifts, its shoulders slightly hunched, and its gaze lowers, as if it’s looking inward. A faint mist, barely perceptible, begins to swirl around its base, a quiet aura of introspection.",
          "yellow", TEXT_SPEED, "")
      spd += 1
      hp -= 1
    case "2":
      lbl(
          "The mannequin’s hands, ever so slightly, begin to flicker with a faint, fiery glow, a warmth radiating from the palm that fades as quickly as it appears. The texture of its surface becomes subtly more cracked, as if a hidden pressure is building just beneath the skin.",
          "yellow", TEXT_SPEED, "")
      atk += 1
      hp -= 1
      mrl -= 1
    case "3":
      lbl(
          "The mannequin’s limbs stretch and twist, reaching out in all directions, fingers brushing against the void as if grasping for something unseen. Its head tilts in curiosity, gazing far into the distance with an unyielding determination, though it remains grounded.",
          "yellow", TEXT_SPEED, "")
      dfc += 1
      atk -= 1
    case "4":
      lbl(
          "The edges of the mannequin’s form seem to blur just a little, becoming less distinct, as if the boundary between it and the void is fading. There is a calmness in its posture, no tension in the shoulders or neck, only an almost imperceptible exhale that seems to emanate from it.",
          "yellow", TEXT_SPEED, "")
      mna += 1
      dfc -= 1
    case "5":
      lbl(
          "The mannequin’s posture stiffens imperceptibly, and its fingers twitch as if they’re clenching into fists. A faint, pulsing glow begins to emanate from its chest, as though the mannequin's heart beats with the rhythm of its defiant will. The air around it feels slightly charged, as if anticipation hangs in the balance.",
          "yellow", TEXT_SPEED, "")
      atk += 1
      spd -= 1

  print("\n\n")
  choice = getResponse("What is the most valuable thing in life?", [
      "Love and connection.", "Knowledge and understanding.",
      "Freedom and choice", "Honour and integrity.",
      "Survival and self preservation."
  ])

  match choice:
    case "1":
      lbl(
          "The clothing begins to stitch itself from the mannequin’s bare skin, weaving delicate, glowing threads that form an intricate web of silk and lace. The fabric pulses softly, as if alive with the warmth of connection, each stitch symbolizing a bond slowly taking shape.",
          "yellow", TEXT_SPEED, "")
      purpose = "The Caregiver."
      atk += 1
    case "2":
      lbl(
          "Threads of deep, dark fabric wind themselves around the mannequin, embroidering arcane symbols and geometric patterns. The material shimmers faintly, as the garment forms with meticulous precision—each seam a piece of wisdom being sewn into existence.",
          "yellow", TEXT_SPEED, "")
      purpose = "The Scholar."
      mna += 1
    case "3":
      lbl(
          "The mannequin’s bare body is soon wrapped in flowing, iridescent fabrics that shift color like the sky. The material seems to emerge from thin air, constantly shifting and rearranging, creating an outfit that feels as free and uncontained as the choices it represents.",
          "yellow", TEXT_SPEED, "")
      purpose = "The Rebel."
      spd += 1
    case "4":
      lbl(
          "Rich fabrics of velvet and brocade stitch themselves into the mannequin’s form, forming a regal tunic adorned with symbols of justice. The seams tighten and align, creating a garment that radiates strength and unwavering moral clarity with every new stitch.",
          "yellow", TEXT_SPEED, "")
      purpose = "The Guardian."
      hp += 1
    case "5":
      lbl(
          "Rugged leather and tough, practical fabrics grow from the mannequin’s skin, stitching themselves into a form-fitting suit. Reinforced seams and straps appear, shaping an outfit that speaks of readiness and survival, adapting with each layer for protection and resilience.",
          "yellow", TEXT_SPEED, "")
      purpose = "The Survivor."
      dfc += 1

  print("\n\n")
  lbl(
      "The void is still vast, the stars still flicker with distant, timid light. You stand before your creation, now fully formed, the weight of your choices pressing in on you. The darkness stretches endlessly in every direction, but for the first time, you feel the stirrings of something within you—a sense that, perhaps,",
      "clear", TEXT_SPEED, "")
  lbl(" this form was not created to stand still", "yellow", 0.1, "")
  lbl(".", "clear", TEXT_SPEED, "")
  return name, sex, origin, dfc, atk, spd, hp, mna, mrl, purpose

def loadScreen():
  """Displays the load screen and allows the player to load, delete, or create a new game."""
  save_files = persistance.getGameIds()
  if save_files:
    lbl("Available save files:\n", "clear", TEXT_SPEED, 0.1)
    for i, (save_id, save_name) in enumerate(save_files):
      lbl(f"{i+1}. {save_name}\n", "yellow", 0.1, "")
    while True:
      try:
        choice = int(input("Select a save file (enter a number): "))
        if 1 <= choice <= len(save_files):
          selected_save_id = save_files[choice - 1][0]
          break
        else:
          print("Invalid choice. Please enter a valid number.")
      except ValueError:
        print("Invalid input. Please enter a number.")
    while True:
      print("What would you like to do with this save file?")
      print("1. Load")
      print("2. Delete")
      print("3. Choose a different save file")
      choice = int(input("Enter your choice (1-3): "))
      if choice == 1:
        player_data = persistance.loadGame(save_files[choice - 1][1])
        if player_data:
          # Use the loaded player data
          print(f"Loaded save file: {save_files[choice - 1][1]}")
          return player_data
        else:
          print(f"Error loading save file: {save_files[choice - 1][1]}")
      elif choice == 2:
        persistance.deleteGame(selected_save_id)
        print(f"Save file {save_files[choice - 1][1]} deleted.")
      elif choice == 3:
        break
      else:
        print("Invalid choice. Please enter a number between 1 and 3.")
  else:
    print("No save files found.")
    print("Starting a new game...")
    return None


# ──────────────────────────────────────────────────────────────────────
# ──────────────────────────────── main ────────────────────────────────
# ──────────────────────────────────────────────────────────────────────


player = None
player = loadScreen()


while True:
  if player is None:
    name, sex, origin, dfc, atk, spd, hp, mna, mrl, purpose = void()
    player = Player(name, sex, origin, 16, dfc, spd, atk, hp, mna, mrl)
    player.status()
  if player.current_location == "void":
    match player.origin:
      case "Born into a war-torn land, shaped by conflict.":
        pass
      case "Raised in the archives of a vast library or as an apprentice to a mysterious mentor.":
        pass
      case "Born in the alleys of a bustling city, surviving by wit and guile.":
        RS.RogueSpawn()
      case "A village guardian or a member of a sacred order.":
        pass
      case "Exiled from a forgotten place, seeking redemption or purpose.":
        pass
      case "Raised in a city of culture or as a dreamer in a humble village.":
        pass
      case "A blank slate, allowing for a fully player-defined backstory.":
        pass
    save_player_data(player)
  else:
    match player.current_location:
      case "RogueSpawn":
        RS.RogueSpawn()
