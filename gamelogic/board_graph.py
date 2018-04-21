#!/usr/bin/env python3
import json

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
modes = Enum(["normal", "donut", "cube"])

class Board:
    """
    Size should be given in a tuple of (m_1, ...m_n)
    Mode should be an enum defined above, such as mode.normal or mode.donut
    """
    def __init__(self, dim, mode):
        self.dim = dim
        self.mode = mode
        self.id = 0
        self.dict = {}
        self.fill_board((), dim)

    def __repr__(self):
        return json.dumps(self.dict)

    def fill_board(self, idxs, dim):
        if not dim:
            self.dict.update({self.id: (idxs, {})})
            self.id += 1
            return
        for i in range(dim[0]):
            self.fill_board((i, *idxs), dim[1:])


if __name__ == "__main__":
    b = Board((4,4,4), modes.normal)
    print(b)
