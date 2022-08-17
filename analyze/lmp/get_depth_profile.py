import numpy as np
import pandas as pd
from ase.io import lammpsdata

def get_depth_profile(
        path2dumpfile: str,
        x_width: float,
        y_width: float,
        z_width: float,
        bins: int =200,
        step: int =0.5,
        moving_average_with_depth_interval: int =3
    ) -> pd.DataFrame:
    """Calculate depth profile for given lmp dump file

    Args:
        path2dumpfile (str): path to lmp dumpfile
        bins (int, optional): number of bins. Defaults to 200.
        step (int, optional): interval between each bin. Defaults to 0.5.
        moving_average_with_depth_interval (int, optional): depth interval for moving average. Defaults to 3.

    Returns:
        pd.DataFrame: depth[ang], ma(moving average)[cm^-3]
    """
    ang3tocm3 = 10e24
    structure = lammpsdata.read_lammps_data(file=path2dumpfile, style='atomic')
    position_df = pd.DataFrame(data=structure.positions, columns=['x', 'y', 'z'])
    z_position = position_df['z'].values

    # convert z-position to depth
    depth = z_position - z_width

    upper = step * bins - z_width
    linspace = np.linspace(upper, -z_width, bins + 1)
    
    width = step
    density_list = []
    for i in linspace:
        n_atom_in_range = ((i - width/2 < depth) & (depth < i + width/2)).sum()
        vol = x_width * y_width * width
        density = n_atom_in_range / vol * ang3tocm3
        density_list.append(density)
    
    df = pd.DataFrame(data=np.stack([linspace, density_list]).T, columns=['linspace', 'density'])
    df['ma'] = df['density'].rolling(int(moving_average_with_depth_interval / step + 1), center=True).mean()
    df.dropna(axis=0, inplace=True)
    return df