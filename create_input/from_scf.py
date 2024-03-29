from scf.qelattice import get_qel
from scf.scf_util import flatten


class N2p2ScfParser:
    def __init__(self, path2scfout, is_comment=True) -> None:
        self.qel = get_qel(path2scfout)
        self.path2scfout = path2scfout
        self.is_comment = is_comment
        
    @property
    def n2p2_comment(self):
        return f'comment {self.path2scfout} .'

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
        energy = self.qel.get_energy()
        return f'energy {energy}'
    
    @property
    def n2p2_charge(self):
        return 'charge 0.0'
    
    @property
    def n2p2_block(self):
        if self.is_comment:
            block = [
                'begin',
                self.n2p2_comment,
                self.n2p2_cell,
                self.n2p2_atom,
                self.n2p2_energy,
                self.n2p2_charge,
                'end \n' 
            ]
        else:
            block = [
                'begin',
                self.n2p2_cell,
                self.n2p2_atom,
                self.n2p2_energy,
                self.n2p2_charge,
                'end \n' 
            ]
        block = flatten(block)
        return block    