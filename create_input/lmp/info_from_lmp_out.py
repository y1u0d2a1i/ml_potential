from distutils.command.config import dump_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from ml_utils.util import remove_empty_from_array, get_param_idx


class LammpsLogParser:
    def __init__(self, path2target, dump_filename=None) -> None:
        self.path2target = path2target
        self.lines = self.get_log_lines()
        if dump_filename is not None:
            self.dump_filename = dump_filename
            self.dump_lines = self.get_dump_lines()
        
    
    def get_log_lines(self) -> list[str]:
        lmp_out_filename = 'log.lammps'
        if not os.path.exists(os.path.join(self.path2target, lmp_out_filename)):
            raise FileNotFoundError('there is no log.lammps')
        
        with open(os.path.join(self.path2target, lmp_out_filename), mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
        return lines
    
    
    def get_dump_lines(self) -> list[str]:
        if not os.path.exists(os.path.join(self.path2target, self.dump_filename)):
            raise FileNotFoundError(f'there is no {self.dump_filename}')
        with open(os.path.join(self.path2target, self.dump_filename), mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
        return lines
    
    
    def get_log_df(self) -> pd.DataFrame:
        info_header_idx = get_param_idx('TotEng', self.lines)
        info_from_lmp_log = [remove_empty_from_array(line.split(' ')) for line in self.lines[info_header_idx: info_header_idx+2]]
        lmp_log_df = pd.DataFrame(columns=info_from_lmp_log[0], data=info_from_lmp_log[1:], dtype=float)
        return lmp_log_df
    
    
    def get_energy(self) -> float:
        df = self.get_log_df()
        total_energy = df['TotEng'].values[0] 
        return total_energy
    
    
    def get_dump_df(self) -> pd.DataFrame:
        num_atom_idx = get_param_idx('NUMBER OF ATOMS', self.dump_lines)
        atom_idx = get_param_idx('ITEM: ATOMS', self.dump_lines)

        num_atom = int(self.dump_lines[num_atom_idx+1])
        atom_header = self.dump_lines[atom_idx].split(' ')[2:]
        atom_coords = [i.split(' ') for i in self.dump_lines[atom_idx+1: atom_idx+1+num_atom]]
        atom_coords = [list(map(float, i)) for i in atom_coords]
        atom_df = pd.DataFrame(data=atom_coords, columns=atom_header)
        return atom_df
    
    
    def get_force(self) -> np.array:
        df = self.get_dump_df()
        return df[['fx', 'fy', 'fz']].values
    
    