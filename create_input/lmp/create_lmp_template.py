from ase.io import read
import os
import shutil
from ml_utils.util import flatten


class CreateLammpsTemplate():
    def __init__(self, path2scf, path2template, path2out) -> None:
        self.path2scf = path2scf
        self.path2template = path2template
        self.path2out = path2out
        self.structure = read(os.path.join(path2scf, 'scf.in'), format='espresso-in')
    
    
    def get_lmp_template_line(self, filename='zbl.in') -> list[str]:
        """get lammps template line

        Args:
            filename (str, optional): name of template filename. Defaults to 'zbl.in'.

        Returns:
            str: list of lammps template line
        """
        with open(os.path.join(self.path2out, filename), mode='r') as f:
            l_strip = [s.strip() for s in f.readlines()]
        return l_strip
    
    @staticmethod
    def get_lattice_start_idx(lines: list[str]) -> int:
        start_idx = None
        for i, line in enumerate(lines):
            if 'lattice custom 1.0 &' in line:
                start_idx = i
                break
        return start_idx
    
    
    def get_cell_for_lmp(self) -> list[str]:
        cell = list(map(lambda x: list(x), self.structure.get_cell()))
        cell[0].insert(0, 'a1')
        cell[1].insert(0, 'a2')
        cell[2].insert(0, 'a3')
        for i in cell:
            i.append('&')
        cell = [' '.join(list(map(str, i))) for i in cell]
        return cell
    
    
    def get_atoms_for_lmp(self) -> list[str]:
        atoms = []
        for atom in list(map(lambda x: list(x), self.structure.get_scaled_positions())):
            atom = list(map(lambda x: str(round(x, 6)), atom))
            atom.insert(0, 'basis')
            atom.append('&')
            atoms.append(' '.join(atom))
        return atoms
        
        
    def create_template(self, template_filename: str, out_filename: str):
        # copy lammps template file to output directory
        shutil.copy(os.path.join(self.path2template, 'zbl.in'), self.path2out)

        l_strip = self.get_lmp_template_line(filename=template_filename)
        start_idx = self.get_lattice_start_idx(l_strip)
        cell = self.get_cell_for_lmp()
        atoms = self.get_atoms_for_lmp()
        
        # insert cell and atoms to lmp template lines
        l_strip.insert(start_idx+1, cell)
        l_strip.insert(start_idx+2, atoms)
        
        l_strip = flatten(l_strip)
        with open(os.path.join(self.path2out, out_filename), mode='w') as f:
            f.write('\n'.join(l_strip))
    
    @classmethod
    def run(
        cls,
        path2scf,
        path2template,
        path2out,
        template_filename,
        out_filename
        ):
        try:
            obj = cls(
                path2scf=path2scf,
                path2out=path2out,
                path2template=path2template
            )
            obj.create_template(template_filename=template_filename, out_filename=out_filename)
            print(f'A lammps template file is successfully created to [{path2out}]')
        except Exception as e:
            raise e
        