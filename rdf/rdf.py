import numpy as np
import os

from ase.io import read
from ovito.modifiers import CoordinationAnalysisModifier
from ovito.pipeline import StaticSource, Pipeline
from ovito.io.ase import ase_to_ovito


def calc_rdf(path2scf, rcut, bins):
    structure = read(os.path.join(path2scf, 'scf.in'), format='espresso-in')
    pipeline = Pipeline(source = StaticSource(data=ase_to_ovito(structure)))
    modifier = CoordinationAnalysisModifier(cutoff=rcut, number_of_bins=bins, partial=True)
    pipeline.modifiers.append(modifier)
    rdf_table = pipeline.compute().tables['coordination-rdf']

    return rdf_table.xy()


def get_rdf_val(rcut, bins, all_dirs):
    rdf_val_list = []
    for path2scf in all_dirs:
        rdf_table = calc_rdf(path2scf, rcut, bins)
        rdf_val_list.append(rdf_table[:, 1])
    linspace = rdf_table[:, 0]

    return linspace, np.array(rdf_val_list)        