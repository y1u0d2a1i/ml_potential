from scf.scf_util import flatten
from create_input.from_scf import N2p2ScfParser
from create_input.lmp.info_from_lmp_out import LammpsLogParser
from scf.get_lattice_info import QELattice
from scf.get_relax_lattice_info import RelaxQELattice



class ScfMinusLammpsN2p2():
    def __init__(self, path2scfout, dump_filename, is_comment=True, is_relax=False) -> None:
        self.qel = RelaxQELattice(path2scfout) if is_relax else QELattice(path_to_target=path2scfout)
        self.num_atom = self.qel.num_atom
        self.path2scfout = path2scfout
        self.is_comment = is_comment
        self.lmp_log_parser = LammpsLogParser(path2target=path2scfout, dump_filename=dump_filename)
        
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
        force = self.get_calced_force()
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
        energy = self.get_calced_energy()
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
    
    
    def get_calced_force(self):
        force = self.qel.get_force()
        force_from_lmp = self.lmp_log_parser.get_force()
        return force - force_from_lmp
    
    
    def get_calced_energy(self):
        energy = self.qel.get_energy()
        energy_from_lmp = self.lmp_log_parser.get_energy()
        return energy - energy_from_lmp