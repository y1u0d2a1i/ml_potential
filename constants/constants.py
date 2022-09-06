from glob import glob
import pandas as pd
from ml_utils.util import flatten
from scf.get_lattice_info import QELattice
from scf.qelattice import get_qel


def get_path2data():
    return '/Users/y1u0d2/desktop/Lab/data/qe_data/Si'


def get_silicon_all_scf_data():
    path2data = get_path2data()
    all_path = []
    material_dirs = glob(f'{path2data}/mp-*')
    for material_dir in material_dirs:
        structures = list(set(glob(f'{material_dir}/*')) -
                        set(glob(f'{material_dir}/*.*')))
        all_path.append(structures)
    all_path = list(flatten(all_path))
    return all_path


def get_all_structure_info():
    all_dirs = get_silicon_all_scf_data()
    result = []
    for path in all_dirs:
        qel = get_qel(path)
        mpid = list(filter(lambda x: 'mp-' in x, path.split('/')))[0]
        n_atom = qel.num_atom
        result.append([mpid, n_atom])
    df = pd.DataFrame(data=result, columns=['mpid', 'n_atom'])
    pt = pd.pivot_table(df, index=['mpid', 'n_atom'], aggfunc=len, margins=True)
    return pt