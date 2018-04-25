import json
from operator import itemgetter
import code

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
modes = Enum(["normal", "donut", "cube", "square", "triangle"])

class Board:
    def __init__(self):
        pass

    """
    Size should be given in a tuple of (m_1, ..., m_n)
    Mode should be an enum defined above, such as mode.normal or mode.donut
    """

    """
    constructor for a board based on square grid
    will create id's and id relations based on coordinates
    """
    @classmethod
    def square_grid(cls, dim):
        inst = cls()
        inst.dim = dim
        inst.mode = modes.square
        inst.nodes = 0
        inst.pieces = {}
        inst.name_to_id = {}
        inst.id_to_name = {}
        inst.edge_neighbors = {}
        inst.vertex_neighbors = {}
        inst.pass_through = {}
        inst.fill_board((), dim)
        inst.add_square_connections()
        return inst

    @classmethod
    def triangle_hex(cls, dim):
        inst = cls()
        inst.dim = dim
        inst.dict = {}
        for i in [dim[0] + ceil(i/2) for i in range(dim[1])] + [dim[0]*2-i for i in range(dim[1])]:
            print(i)
            inst.dict.update({ i: [] })
        return inst

    def print_square(self):
        string = ""
        j = 0
        for i in sorted(self.dict, key=itemgetter(0, 1)):
            if j != i[0]:
                print(string)
                string = ""
            string += "X" if (i[0]+i[1])%2 == 1 else "O"
        print(string)

    def __repr__(self):
        return str(self.id_to_name)

    def triangle_hex_fill(self, idxs, dim):
        pass

    def fill_board(self, idxs, dim):
        """git clone https://github.com/Wramberg/TerminalView.git $HOME/.config/sublime-text-3/Packages/TerminalView
        Adds nodes to dict for every coordinate-permutation in a tuple of form (m_1, ..., m_n)
        """
        if not dim:
            self.name_node(idxs, self.nodes)
            self.nodes += 1
            return
        for i in range(dim[0]):
            self.fill_board((i, *idxs), dim[1:])

    def name_node(self, name, id):
        self.name_to_id.update({name: id})
        self.id_to_name.update({id: name})
        self.vertex_neighbors.update({id: []})
        self.edge_neighbors.update({id: []})
        self.pass_through.update({id: []})

    def add_square_connections(self):
        code.interact(local=dict(globals(), **locals()))
        for k in self.name_to_id.keys():
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
            self.edge_neighbors[k] = self.edge_neighbors[k] + neighbors

if __name__ == "__main__":
    b = Board.square_grid((4,4))
    print(b)
    b.print_square()
    c = Board.triangle_hex((4,4))
    print(c)