from secrets import token_urlsafe

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


def generate_random_pass(length: int = 12):
    return token_urlsafe(length)
