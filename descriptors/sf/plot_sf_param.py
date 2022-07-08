from descriptors.sf.sf_function import SymmetryFunction
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_sf_radial(param: dict, rmax: float, ax) -> None:
    """
    plot radial sf from param({eta: , rs: , rcut: })
    """
    sf = SymmetryFunction()
    r_ij = np.linspace(0, rmax, 100)
    ax.set_title(f'symmetry function parameters')
    ax.set_xlabel(f'r(Å)')
    ax.set_ylabel(f'radial symmetry function : G2')
    sf_value = [sf.radial_symmetry_function_2(eta=param['eta'], r_ij=k, r_shift=param['rs'], r_cutoff=param['rcut']) for k in r_ij]
    ax.plot(r_ij, sf_value, label=f'η: {param["eta"]}, Rs: {param["rs"]}')
