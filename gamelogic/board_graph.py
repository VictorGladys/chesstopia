#!/usr/bin/env python3
import json
from operator import itemgetter
# for debugging: 'code.interact(local=dict(globals(), **locals()))'
if __name__ == '__main__':    
    from pieces import *
    from player import *
import code 
from termcolor import colored
import pprint

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
modes = Enum(["normal", "donut", "cube", "square", "triangle"])

class Board:
    def __init__(self, mode):
        self.mode = mode
        self.pieces = {}
        self.name_to_id = {}
        self.id_to_name = {}
        self.edge_neighbors = {}
        self.vertex_neighbors = {}
        self.pass_through = {}
        self.promotion_row = []
        self.en_passant = {}
        self.checked_squares = {}
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
        print(dim)
        edge_rules = [((0, 1), (0, -1)), ((-1, 0), (1, 0))]
        vertex_rules = [((-1, -1), (1, 1)), ((-1, 1), (1, -1))]
        
        inst = cls(modes.square)
        inst.dim = dim
        inst.nodes = 0
        # code.interact(local=dict(globals(), **locals()))
        inst.fill_board((), dim)
        inst.add_coordinate_connections(edge_rules, vertex_rules)
        inst.promotion_row = [ inst.name_to_id[( x, y )] for y in [0, dim[1]-1 ] for x in range(dim[0]) ]
        return inst

    @classmethod
    def triangle_hex(cls, dim):
        inst = cls()
        inst.dim = dim
        inst.dict = {}
        for i in [dim[0] + math.ceil(i/2) for i in range(dim[1])] + [dim[0]*2-i for i in range(dim[1])]:
            print(i)
            inst.dict.update({ i: [] })
        return inst

    def print_square_basic(self):
        for y in range(self.dim[1]):
            string = str(self.dim[1] - 1 - y) + ' '
            for x in range(self.dim[0]):
                if self.name_to_id[(x, y)] in self.pieces.keys():
                    string += self.pieces.get(self.name_to_id[(x, y)]).alias
                elif (x + y) % 2 == 0:
                    string += 'X'
                else:
                    string += 'O'
            print(string)

    def print_square(self):
        for y in range(self.dim[1]):
            print(str(self.dim[1] - 1 - y) + ' ', end = '')
            for x in range(self.dim[0]):
                try: 
                    piece = self.pieces[self.name_to_id[(y, x)]]
                    alias = piece.alias
                    piececolor = piece.owner.color
                except KeyError: 
                    alias = ' '
                    piececolor = 'white'
                if (x + y) % 2 == 0:
                    print(colored(alias, piececolor, 'on_white'), end = '')
                else:
                    print(colored(alias, piececolor), end = '')
            print('')
        print('')
        print('  01234567')

                    



    def __repr__(self):
        return str(self.id_to_name)

    def triangle_hex_fill(self, idxs, dim):
        pass

    def fill_board(self, idxs, dim):
        """
        Adds nodes to dict for every coordinate-permutation in a tuple of form (m_1, ..., m_n)
        """
        id = 0
        for x in range(dim[0]):
            for y in range(dim[1]):
                self.name_node((x, y), id)
                id += 1
        # if not dim:
        #     self.name_node(idxs, self.nodes)
        #     self.nodes += 1
        #     return
        # for i in range(dim[0]):
        #     print(dim)
        #     self.fill_board((i, *idxs), dim[1:])
        #     # code.interact(local=dict(globals(), **locals()))

    def name_node(self, name, id):
        self.name_to_id.update({name: id})
        self.id_to_name.update({id: name})
        self.vertex_neighbors.update({id: []})
        self.edge_neighbors.update({id: []})

    def checked(self, location, owner):
        pass
        # return location in self.id_to_name.keys() and self.board.checked_squares[location].

    def legal(self, location, owner):
        return location in self.id_to_name.keys() and (self.pieces.get(location) == None or self.pieces[location].owner != owner)

    def empty(self, location):
        return location in self.id_to_name.keys() and location not in self.pieces.keys()

    def add_coordinate_connections(self, edge_rules, vertex_rules):
        '''
        adds id connections based on coordinate transformation tuples
        '''
        for k,v in self.name_to_id.items():
            for pass_through_set in edge_rules:
                options = [ tuple(map(sum, zip(k, set))) for set in pass_through_set ]
                allowed_options = []
                for set in options:
                    try: allowed_options.append(self.name_to_id[set])
                    except: pass

                if len(allowed_options) >= 2:
                    for i in allowed_options:
                        self.pass_through.update({ ( i , v ) : [ x for x in allowed_options if x != i ] })
                self.edge_neighbors[v] += allowed_options

# for item in [[item in dict] for item in list]:          

if __name__ == "__main__":
    b = Board.square_grid((4,4))
    print(b)
    p1 = Player('test', 'red')
    p2 = Player('test2', 'green')
    r = Rook(p1, b, 1)
    r2 = Rook(p2, b, 12)
    b.print_square()
    code.interact(local=dict(globals(), **locals()))
    # c = Board.triangle_hex((4,4))
    # print(c)
