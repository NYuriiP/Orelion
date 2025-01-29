game_map = {
    "void" : ["RogueSpawn", "WarriorSpawn", "BardSpawn", "MageSpawn", "BastionSpawn", "OutlawSpawn", "NullSpawn"],
    # These area's will be around the rogue spawn, starting in "RogueSpawn".
    "RogueSpawn" : ["LiuriaCityGate", "LiuriaForest", "FrozenWilds1", "LiuriaOutpost1"], # Starting options for rogue.
    "LiuriaCityGate" : ["RogueSpawn", "LiuriaStreets1"], # This will have continuity later.
    "LiuriaForest" : ["RogueSpawn", "FrozenForest1"],
    "FrozendWilds1" : ["RogueSpawn", "FrozenWilds2", "FrozenWilds3"],
    "LiuriaOutpost1" : ["RogueSpawn", "LiuriaCityGate"],
    "LiuriaStreets1" : ["LiuriaCityGate", "LiuriaTavern", "LiuriaStreets2"],
    "LiuriaTavern" : ["LiuriaStreets1"],
    "LiuriaStreets2" : ["LiuriaStreets1", "LiuriaCityCentre"],
    "LiuriaCityCentre" : ["LiuriaStreets2", "LiuriaMarket", "LiuriaInn", "LiuriaGuildHall", "LiuriaStreets3", "LiuriaStreets4"],
    "LiuriaMarket" : ["LiuriaCityCentre", "LiuriaShop1", "LiuriaShop2", "LiuriaBazaar", "LiuriaShop3", "LiuriaShop4"],
    "LiuriaShop1" : ["LiuriaMarket"],
    "LiuriaShop2" : ["LiuriaMarket"],
    "LiuriaShop3" : ["LiuriaMarket"],
    "LiuriaShop4" : ["LiuriaMarket"],
    "LiuriaBazaar" : ["LiuriaMarket"],
    "LiuriaInn" : ["LiuriaCityCentre"],
    "LiuriaGuildHall" : ["LiuriaCityCentre"],
    "LiuriaStreets3" : ["LiuriaCityCentre", "LiuriaLibrary"],
    "LiuriaStreets4" : ["LiuriaCityCentre", "LiuriaStreets5", "LiuriaAlleyWay"],
    "LiuriaAlleyWay" : ["LiuriaStreets4"],
    "LiuriaLibrary" : ["LiuriaStreets3"],
    "LiuriaStreets5" : ["LiuriaGateway"],
    "LiuriaCastle" : ["LiuriaCitySquare", "LiuriaThroneRoom"],
}
