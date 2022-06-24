from matplotlib.pyplot import cla
import pandas as pd
import numpy as np
import glob
from scf.get_lattice_info import QELattice
from scf.scf_util import flatten


class N2p2ScfParser:
    def __init__(self, path2scfout) -> None:
        self.qel = QELattice(path_to_target=path2scfout)
    
    @property
    def n2p2_cell(self):
        line = []
        cell = self.qel.get_cell()
        for l_vec in cell:
            l_vec = [str(i) for i in list(l_vec)]
            tmp = ' '.join(l_vec)
            line.append(f'lattice {tmp}')
        return line
    
    @property
    def n2p2_atom(self):
        line = []
        coord = self.qel.get_coord()
        force = self.qel.get_force()
        species = 'Si'
        for c, f in zip(coord, force):
            c = [str(i) for i in list(c)]
            f = [str(i) for i in list(f)]
            tmp_c = ' '.join(c)
            tmp_f = ' '.join(f)
            line.append(f'atom {tmp_c} {species} 0 0 {tmp_f}')
        return line
    
    @property
    def n2p2_energy(self):
        return f'energy {energy}'
    
    @property
    def n2p2_charge(self):
        return 'charge 0.0'
    
    @property
    def n2p2_block(self):
        block = [
            'begin',
            self.n2p2_cell,
            self.n2p2_atom,
            self.n2p2_energy,
            self.n2p2_charge,
            'end' 
        ]
        block = flatten(block)
        return block    