class Constant():

    def demo_raid_grops(tank, heal, dd):
        users = {}
        for t in range(1, (tank + 1)):
            users[f'Tank {t}'] = [1,0,0]
        for t in range(1, (heal + 1)):
            users[f'Heal {t}'] = [0,1,0]
        for t in range(1, (dd + 1)):
            users[f'D_D {t}'] = [0,0,1]
        return users