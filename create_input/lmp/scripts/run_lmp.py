from ast import Return
from glob import glob
from ml_utils.util import  flatten
import subprocess
import os
from constants.constants import get_silicon_all_scf_data


path2data = '/Users/y1u0d2/desktop/Lab/data/qe_data/Si'

path2alldata = get_silicon_all_scf_data()

for path in path2alldata:
    try:
        # if os.path.exists(os.path.join(path, 'dump.out')):
        #     print(f'dump.out already exists: {path}')
        #     continue
        os.chdir(path)
        process = subprocess.Popen(f'lmp -in zbl.in', shell=True)
        process.wait()
    except:
        print(path)
