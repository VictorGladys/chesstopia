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
    Size should be given in a tuple of (m_1, ..., m_n)
    Mode should be an enum defined above, such as mode.normal or mode.donut
    """
    def __init__(self, dim, mode):
        self.dim = dim
        self.mode = mode
        self.id = 0
        self.dict = {}
        self.fill_board((), dim)
        self.add_connections()

    def __repr__(self):
        return str(self.dict)

    def fill_board(self, idxs, dim):
        """
        Adds nodes to dict for every coordinate-permutation in a tuple of form (m_1, ..., m_n)
        """
        if not dim:
            self.dict.update({idxs: []})
            self.id += 1
            return
        for i in range(dim[0]):
            self.fill_board((i, *idxs), dim[1:])

    def add_connections(self):
        for k, v in self.dict.items():
            neighbors = []
            for i in range(len(k)):
                tmp = list(k)
                tmp[i] += 1
                if tmp[i] <= len(k) + 1:
                    neighbors.append(tmp)
                tmp = list(k)
                tmp[i] -= 1
                if tmp[i] >= 0:
                    neighbors.append(tmp)
            self.dict[k] = self.dict[k] + neighbors

if __name__ == "__main__":
    b = Board((4,4), modes.normal)
    print(b)
