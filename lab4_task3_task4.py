class BaseClass:
    __age: int = 1
    def print_method(self, msg: str):
        print(f'Remember, son! {msg}')

    def laugh(self):
        print('Uhaha')

    def __init__(self, age: int = 90):
        self.__age = age


class InheritClass(BaseClass):
    def print_method(self, msg: str):
        super().laugh()  # or it can be self.laugh()
        print(f'Ok, boomer. {msg}')

    def swear(self, msg: str, kind=True):
        self.print_method(msg) if kind else super().print_method(msg)
        super().print_method(msg) if kind else self.print_method(msg)

    def grumble(self):
        print(f"I'm already {self._BaseClass__age}? Oh God...")

    def __init__(self, age: int = 16):
        super().__init__(age)


man = InheritClass()
# man.swear('You loser!')
man.grumble()
