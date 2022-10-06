import numpy as np
import collections
from constants.constants import get_silicon_all_scf_data
from create_input.from_scf_minus_lmp import ScfMinusLammpsN2p2
from create_input.from_scf import N2p2ScfParser
from scf.qelattice import get_qel


def get_filtered_structure_path_by_energy(energy_threshold: float) -> list[str]:
    all_dirs = get_silicon_all_scf_data()

    filtered_data = []
    removed_data = []
    for d in all_dirs:
        try:
            n2p2_obj = ScfMinusLammpsN2p2(
                path2scfout=d,
                dump_filename='dump.out',
                is_comment=True
            )
            if n2p2_obj.get_calced_energy() / n2p2_obj.num_atom > energy_threshold:
                filtered_data.append(d)
            else:
                structure_id = list(filter(lambda x: 'mp-' in x, d.split('/')))[0]
                removed_data.append(structure_id)
        except:
            continue
    
    num_removed_data = len(all_dirs) - len(filtered_data)

    collection = collections.Counter(removed_data)
    print(dict(collection))
    print(f'{num_removed_data} structures were removed')
    return filtered_data


def get_filtered_structure_path_by_force(force_threshold: float, is_zbl=True) -> list[str]:
    all_dirs = get_silicon_all_scf_data()

    filtered_data = []
    removed_data = []
    for d in all_dirs:
        try:
            if is_zbl:
                n2p2_obj = ScfMinusLammpsN2p2(
                    path2scfout=d,
                    dump_filename='dump.out',
                    is_comment=True
                )
                force = n2p2_obj.get_calced_force()
            else:
                qel = get_qel(d)
                force = qel.get_force()

            if np.all(np.abs(force) < force_threshold):
                filtered_data.append(d)
            else:
                structure_id = list(filter(lambda x: 'mp-' in x, d.split('/')))[0]
                removed_data.append(structure_id)
        except:
            continue
    
    num_removed_data = len(all_dirs) - len(filtered_data)

    collection = collections.Counter(removed_data)
    print(dict(collection))
    print(f'{num_removed_data} structures were removed')
    return filtered_data