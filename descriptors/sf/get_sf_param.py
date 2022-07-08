import os
from numpy import record
import pandas as pd
from ml_utils.util import remove_empty_from_array
from descriptors.sf.sfparamgen import SymFuncParamGenerator


def get_sf_radial_params(elm: list[str], rcut: float, nb_param_pairs: int) -> pd.DataFrame:
    sfGenerator = SymFuncParamGenerator(elements=['Si'], r_cutoff=rcut)
    sfGenerator.symfunc_type = 'radial'
    sfGenerator.generate_radial_params(rule='imbalzano2018', mode='shift', nb_param_pairs=nb_param_pairs)
    
    lines = get_sf_lines_from_generator(sfGenerator=sfGenerator)
    columns = ['sftype', 'elm1', 'sfnum', 'elm2', 'eta', 'rs', 'rcut']
    df = pd.DataFrame(data=lines, columns=columns)
    df[['eta', 'rs', 'rcut']] = df[['eta', 'rs', 'rcut']].astype(float)
    return df


def get_sf_lines_from_generator(sfGenerator: SymFuncParamGenerator):
    pwd = os.getcwd()
    path2tmp = os.path.join(pwd, 'tmp.txt')
    # 書き込み
    with open(path2tmp, mode='w') as f:
        sfGenerator.write_parameter_strings(fileobj=f)
    # 読み込み
    with open(path2tmp, mode='r') as f:
        l_strip = [s.strip() for s in f.readlines()]
        l_strip = remove_empty_from_array(l_strip)
    l_strip = [remove_empty_from_array(i.split(' ')) for i in l_strip]
    # tmp.txt削除
    os.remove(path2tmp)
    return l_strip


def get_sf_param_dict(df: pd.DataFrame, param_name: list[str]) -> dict:
    params = df[param_name].to_dict(orient=record)
    return params

