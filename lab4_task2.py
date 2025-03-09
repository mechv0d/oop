from typing import Any


class TestClass:
    name: str = None
    attr_0: int = 0
    attr_1: int = 0

    def __init__(self, name, **kwargs):
        self.name = name
        for (k, v) in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'TestClass({self.name}, attr_0={self.attr_0}, attr_1={self.attr_1})'


def find_strongest(array: list[Any], target: str) -> Any:
    sorcerer_dict: dict[Any, int] = {}
    for value in array:
        if isinstance(value, list):
            ss = find_strongest(value, target)
            if ss is not None:
                sorcerer_dict[ss] = getattr(ss, target)
        elif hasattr(value, target):
            sorcerer_dict[value] = getattr(value, target)

    sorcerer_tuples = sorted(sorcerer_dict.items(), key=lambda item: item[1], reverse=True)
    if len(sorcerer_tuples) == 0:
        return None
    return sorcerer_tuples[0][0]


arr = [
    TestClass('Evgenii', attr_0=15, attr_1=37),
    TestClass('Alexei', attr_0=1, attr_1=21),
    TestClass('Artyom', attr_0=17, attr_1=45),
    TestClass('Cepega', attr_0=9, attr_1=62),
]

darr = [
    [TestClass('Nikolai', attr_0=19, attr_1=17), TestClass('Adik', attr_0=4, attr_1=5)],
    [TestClass('Rudolf', attr_0=11, attr_1=11), TestClass('Phoenix', attr_0=37, attr_1=91),
     TestClass('Стафилококк', attr_0=1, attr_1=999)],
    [],
]

print(find_strongest(darr, 'attr_1'))
