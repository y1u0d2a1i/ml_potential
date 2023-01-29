from glob import glob
import pandas as pd
from ml_utils.util import flatten
from scf.get_lattice_info import QELattice
from scf.qelattice import get_qel


def get_path2data():
    return '/Users/y1u0d2/desktop/Lab/data/qe_data/Si'


def create_structure_dict(all_path):
    mpid_list = set([list(filter(lambda x: 'mp-' in x, d.split('/')))[0] for d in all_path])
    all_dirs_dict = {}
    for mpid in mpid_list:
        all_dirs_dict[mpid] = list(filter(lambda x: f'/{mpid}/' in x, all_path))
    return all_dirs_dict


def get_silicon_all_scf_data(as_dict=False):
    path2data = get_path2data()
    all_path = []
    material_dirs = glob(f'{path2data}/mp-*')
    for material_dir in material_dirs:
        structures = list(set(glob(f'{material_dir}/*')) -
                        set(glob(f'{material_dir}/*.*')))
        all_path.append(structures)
    all_path = list(flatten(all_path))

    if as_dict:
        return create_structure_dict(all_path=all_path)
    else:
        return all_path


def get_silicon_all_scf_data_sd(as_dict=False):
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

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-149/atom8/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-1079649/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-165/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-571520/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-92/coord'
    add_structure_path(path, all_dirs)

    path = '/Users/y1u0d2/desktop/Lab/result/qe/Si/mp-149_dimer/coord/01/result'
    all_dirs = all_dirs + glob(f'{path}/scf*')

    if as_dict:
        return create_structure_dict(all_path=all_dirs)
    else:
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