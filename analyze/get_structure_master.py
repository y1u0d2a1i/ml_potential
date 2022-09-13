import pandas as pd
from analyze.n2p2_lattice import N2p2Lattice, get_structures_for_n2p2_lattice


def get_structure_master_df(path2target):
    structures = get_structures_for_n2p2_lattice(path2target, 'input.data')
    path_index_master = []
    for i ,structure in enumerate(structures):
        n2p2_lattice = N2p2Lattice(structure)
        path_index_master.append([i, n2p2_lattice.path, n2p2_lattice.mpid])

    return pd.DataFrame(data=path_index_master, columns=['index', 'path', 'mpid'])