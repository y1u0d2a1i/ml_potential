from glob import glob
import os
import shutil
from ml_utils.util import remove_empty_from_array

def change_nnpdir(lines, path2nnpdir):
    for i, l in enumerate(lines):
        if 'variable nnpDir' in l:
            dir_l = remove_empty_from_array(l.split(' '))
            dir_l[-1] = f'"{path2nnpdir}"'
            lines[i] = ' '.join(dir_l)
            break
    return lines


def make_elastic_dirs(path2n2p2_result: str, path2mechanical_prop_files: str) -> None:
    """make elastic directories in n2p2 result dir

    Args:
        path2n2p2_result (str): path to n2p2 calculation result dir
        path2mechanical_prop_files (str): path to template dir
    """
    path2elastic = os.path.join(path2n2p2_result, 'elastic')
    if not os.path.exists(path2elastic):
        os.mkdir(path2elastic)
    
    weights_files = glob(f'{path2n2p2_result}/weight*')
    for weights_f in weights_files:
        print(weights_f)
        epoch = int(weights_f.split('/')[-1].split('.')[-2])
        path2epoch = os.path.join(path2elastic, f'e_{epoch}')

        # copy mechanical prop files
        if not os.path.exists(path2epoch): shutil.copytree(path2mechanical_prop_files, path2epoch)

        # copy n2p2 files
        shutil.copy(os.path.join(path2n2p2_result, 'input.nn'), path2epoch)
        shutil.copy(os.path.join(path2n2p2_result, 'scaling.data'), path2epoch)
        shutil.copy(os.path.join(path2n2p2_result, weights_f), path2epoch)
        os.rename(os.path.join(path2epoch, weights_f), os.path.join(path2epoch, 'weights.014.data'))

        # change potential.mod
        with open(os.path.join(path2epoch, 'potential.mod'), mode='r') as f:
            lines = [s.strip() for s in f.readlines()]
        changed_lines = change_nnpdir(lines, path2epoch)
        with open(os.path.join(path2epoch, 'potential.mod'), mode='w') as f:
            f.write('\n'.join(changed_lines))