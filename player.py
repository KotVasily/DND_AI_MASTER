import random

class Player:
    def __init__(self, russa, name) -> None:
        """
        russa - Расса
        name - Имя, нужно для определения кто ходит
        """
        self.russa = russa
        self.name = name

    def random_cube(self):
        return f"""d4={random.randint(1, 4)}, d6={random.randint(1, 6)}, d8={random.randint(1, 8)}, d10={random.randint(1, 10)},
          d12={random.randint(1, 12)}, d20={random.randint(1, 20)}"""