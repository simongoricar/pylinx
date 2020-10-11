#################
# Custom class because python is mad
#################
class Integer:
    def __init__(self, value: int):
        self.value = value

    def get(self) -> int:
        return self.value

    def set(self, value: int):
        self.value = value
