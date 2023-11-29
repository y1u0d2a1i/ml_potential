import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_structures_for_n2p2_lattice(path2inputdata, i_filename='input.data'):
    with open(os.path.join(path2inputdata, i_filename), mode='r') as f:
        lines = [s.strip() for s in f.readlines()]

    end_idx_list = [i for i, line in enumerate(lines) if 'end' in line]
    structures = []

    start_idx = 0
    for end_idx in end_idx_list:
        structures.append(lines[start_idx:end_idx+1])
        start_idx = end_idx + 1

    return structures

class N2p2Lattice():
    def __init__(self, structure) -> None:
        self.structure = structure
        self.atom_lines = structure[5:-3]
        self.n_atoms = len(self.atom_lines)
        self.cell = self.get_cell()
        self.vol = self.get_vol()
        self.energy = self.get_energy()
        self.coord = self.get_coord()
        self.force = self.get_force()
        self.mpid = self.get_mpid()
        self.path = self.get_path()

    
    def get_mpid(self):
        try:
            comment = self.structure[1]
            mpid = list(filter(lambda x: 'mp-' in x, comment.split(' ')[1].split('/')))[0]
            return mpid
        except:
            return None
            # return comment.split(' ')[1].split(':')[1]

    
    def get_path(self):
        try:
            comment = self.structure[1]
            return comment.split(' ')[1]
        except:
            return None


    def get_cell(self):
        cell = []
        cell_block = self.structure[2:5]
        for i in cell_block:
            cell.append(list(map(float ,i.split(' ')[1:])))
        return np.array(cell)


    def get_vol(self):
        cell = self.get_cell()
        a = cell[0]
        b = cell[1]
        c = cell[2]
        return round(np.dot(a, np.cross(b,c)), 3)


    def get_energy(self):
        energy = self.structure[-3].split(' ')[-1]
        return float(energy)


    def get_coord(self):
        coord = []
        for atom_line in self.atom_lines:
            coord.append([float(i) for i in atom_line.split(' ')[1:4]])
        return np.array(coord)
    

    def get_force(self):
        force = []
        for atom_line in self.atom_lines:
            force.append([float(i) for i in atom_line.split(' ')[-3:]])
        return np.array(force)