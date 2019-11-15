from dataclasses import dataclass


@dataclass
class DataSoldier:
    name: str
    attack: int
    defence: int
    hp: int


class Soldier:
    def __init__(self, name, attack, defence, hp):
        self.name = name
        self.attack = attack
        self.defence = defence
        self.hp = hp


# Both are the same, but Dataclass auto creates the __init__
x = DataSoldier('Bob', 10, 20, 300)
y = Soldier('Jack', 10, 20, 300)

