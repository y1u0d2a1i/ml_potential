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


def get_silicon_all_scf_data_sd():
    def add_structure_path(path, all_dirs):
        dirs = glob(f'{path}/*')
        for d in dirs:
            scf_dirs = glob(f'{d}/result/scf*')
            if len(scf_dirs) == 0:
                continue
            for scf_d in scf_dirs:
                all_dirs.append(scf_d)
    
    all_dirs = []

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-149/coord/sd'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-1079649/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-165/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-571520/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-92/coord'
    add_structure_path(path, all_dirs)

    return all_dirs

    

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