import glob
import os
from constants.constants import get_silicon_all_scf_data
from create_input.from_scf import N2p2ScfParser
from scf.scf_util import flatten
from create_input.from_scf_minus_lmp import ScfMinusLammpsN2p2


def get_filtered_structure_path(energy_threshold: float) -> list[str]:
    all_dirs = get_silicon_all_scf_data()

    filtered_data = []
    for d in all_dirs:
        is_relax = False
        if os.path.exists(os.path.join(d, 'relax.in')):
            is_relax = True
        try:
            n2p2_obj = ScfMinusLammpsN2p2(
                path2scfout=d,
                dump_filename='dump.out',
                is_comment=True,
                is_relax=is_relax
            )
            if n2p2_obj.get_calced_energy() / n2p2_obj.num_atom > energy_threshold:
                filtered_data.append(d)
        except:
            continue
    
    num_removed_data = len(all_dirs) - len(filtered_data)
    print(f'{num_removed_data} structures were removed')
    return filtered_data