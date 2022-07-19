from glob import glob
from ml_utils.util import flatten


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