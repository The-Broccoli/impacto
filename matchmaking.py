def group_matchmaking(users):
    # Emojis für die Rollen
    TANK_EMOJI = "🟢"
    HEALER_EMOJI = "🔵"
    DAMAGE_EMOJI = "🔴"
    
    # Funktion zum Hinzufügen des Emojis
    def add_emoji(name, roles):
        if roles[0] == 1:
            return f"{TANK_EMOJI} {name}"
        elif roles[1] == 1:
            return f"{HEALER_EMOJI} {name}"
        else:
            return f"{DAMAGE_EMOJI} {name}"
    
    # Sortiere Benutzer nach Rollen
    tanks = []
    healers = []
    damage_dealers = []
    for name, roles in users.items():
        if roles[0] == 1:
            tanks.append(name)
        elif roles[1] == 1:
            healers.append(name)
        else:
            damage_dealers.append(name)
    
    gruppen = []
    restliche_spieler = set(users.keys())
    
    # Erstelle Gruppen mit mindestens einem Tank und einem Healer
    while tanks and healers and len(restliche_spieler) >= 2:
        gruppe = [tanks.pop(0), healers.pop(0)]
        restliche_spieler -= set(gruppe)
        
        # Fülle die Gruppe mit Damage Dealern auf
        while len(gruppe) < 6 and damage_dealers:
            if damage_dealers[0] in restliche_spieler:
                gruppe.append(damage_dealers.pop(0))
                restliche_spieler.remove(gruppe[-1])
            else:
                damage_dealers.pop(0)
        
        gruppen.append(gruppe)
    
    # Verteile übrige Tanks und Healer
    for role in [tanks, healers]:
        for player in role:
            if player in restliche_spieler:
                for gruppe in gruppen:
                    if len(gruppe) < 6:
                        gruppe.append(player)
                        restliche_spieler.remove(player)
                        break
    
    # Erstelle Restgruppen mit übrigen Spielern
    restgruppe = list(restliche_spieler)
    while restgruppe:
        neue_gruppe = restgruppe[:6]
        gruppen.append(neue_gruppe)
        restgruppe = restgruppe[6:]
    
    # Füge Emojis zu den Namen hinzu
    gruppen_mit_emojis = []
    for gruppe in gruppen:
        gruppe_mit_emojis = [add_emoji(name, users[name]) for name in gruppe]
        gruppen_mit_emojis.append(gruppe_mit_emojis)
    
    return gruppen_mit_emojis

# # Beispielaufruf
# users = {
#     'Otomay1':[1,0,0], 'Otomay2':[0,1,0], 'Otomay3':[0,1,0], 'Otomay4':[0,1,0],
#     'Otomay5':[1,0,0], 'Otomay6':[0,1,0], 'Otomay7':[0,0,1], 'Otomay8':[1,0,0],
#     'Otomay9':[0,0,1], 'Otomay10':[0,0,1], 'Otomay11':[0,0,1], 'Otomay12':[0,0,1],
#     'Otomay13':[0,0,1], 'Otomay14':[0,0,1], 'Otomay15':[0,0,1], 'Otomay16':[0,0,1],
#     'Otomay17':[0,0,1], 'Otomay18':[0,0,1], 'Otomay19':[0,0,1],
# }

# ergebnis = group_matchmaking(users)
# # for i, gruppe in enumerate(ergebnis, 1):
# #     print(f"Gruppe {i}: {gruppe}")

# print(ergebnis)