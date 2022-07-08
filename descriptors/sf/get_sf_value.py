import pandas as pd
from dscribe.descriptors import ACSF

class SfFuncVal():
    def __init__(self, path2target=None) -> None:
        self.path2target = path2target


    @classmethod
    def get_g2_value(cls, g2_params: list[float], structure, species, rcut) -> pd.DataFrame:
        columns = cls.get_g2_columns(g2_params)
        acsf = ACSF(
            species=species,
            rcut=rcut,
            g2_params=g2_params,
            periodic=True,
        )
        sf_value = acsf.create(system=structure)
        return pd.DataFrame(data=sf_value, columns=columns)
        
    
    def get_g2_columns(g2_params: list[float])->list[str]:
        columns = [f'eta-{param[0]}_rs-{param[1]}' for param in g2_params]
        columns.insert(0, 'g1')
        return columns