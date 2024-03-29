import pandas as pd
from dscribe.descriptors import ACSF

class SfFuncVal():
    def __init__(self, path2target=None) -> None:
        self.path2target = path2target


    @classmethod
    def get_g2_value(cls, g2_params: list[float], structure, species, rcut, periodic=True) -> pd.DataFrame:
        """get g2_value of symmetry function

        Args:
            g2_params (list[float]): list of parameters which has [eta, rs]
            structure (_type_): ase.Atoms
            species (_type_): species
            rcut (_type_): cutoff radius
            periodic (bool, optional): does apply pbc. Defaults to True.

        Returns:
            pd.DataFrame: _description_
        """
        columns = cls.get_g2_columns(g2_params, rcut)
        acsf = ACSF(
            species=species,
            rcut=rcut,
            g2_params=g2_params,
            periodic=periodic,
        )
        sf_value = acsf.create(system=structure)
        return pd.DataFrame(data=sf_value, columns=columns)
    
    @classmethod
    def get_g4_value(cls, g4_params: list[float], structure, species, rcut, periodic=True) -> pd.DataFrame:
        columns = cls.get_g4_columns(g4_params, rcut)
        acsf = ACSF(
            species=species,
            rcut=rcut,
            g4_params=g4_params,
            periodic=periodic,
        )
        sf_value = acsf.create(system=structure)
        return pd.DataFrame(data=sf_value, columns=columns)
        
    
    def get_g2_columns(g2_params: list[float], rcut)->list[str]:
        columns = [f'eta-{param[0]}_rs-{param[1]}_rcut-{rcut}' for param in g2_params]
        columns.insert(0, 'g1')
        return columns

    def get_g4_columns(g4_params: list[float], rcut)->list[str]:
        columns = [f'eta-{param[0]}_zeta-{param[1]}_lam-{param[2]}_rcut-{rcut}' for param in g4_params]
        columns.insert(0, 'g1')
        return columns