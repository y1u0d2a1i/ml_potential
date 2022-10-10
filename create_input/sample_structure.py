from scf.qelattice import get_qel
import pandas as pd

def remove_duplicated_structures(all_dirs) -> pd.DataFrame:
    """ Sample structure by removing structures 
        which has same atom_energy and atom_vol

    Args:
        all_dirs (list): list of path to scf.out

    Returns:
        pd.DataFrame: sampled dataframe which contains energy vol mpid path
    """
    result = []

    for d in all_dirs:
        try:
            qel = get_qel(d)
            result.append([float(qel.get_energy()), qel.structure_id, int(qel.num_atom), float(qel.get_vol()), d])
        except:
            continue
    
    result_df = pd.DataFrame(data=result, columns=['energy', 'mpid', 'n_atom', 'vol', 'path'])
    result_df['atom_energy'] = result_df['energy'] / result_df['n_atom']
    result_df['atom_vol'] = result_df['vol'] / result_df['n_atom']

    sampled_mpid_df_list = []
    for mpid in result_df.mpid.unique():
        print(mpid)
        mpid_df = result_df.query('mpid == @mpid')
        mpid_df = mpid_df.reset_index(drop=True)
        # round atom_energy and atom_vol
        mpid_df['atom_energy_round'] = round(mpid_df['atom_energy'].copy(), 1)
        mpid_df['atom_vol_round'] = round(mpid_df['atom_vol'].copy(), 1)
        # remove structure which has same atom_energy and atom_vol
        sampled_mpid_df = mpid_df.iloc[mpid_df[['atom_energy_round', 'atom_vol_round']].drop_duplicates().index, :].copy()
        sampled_mpid_df_list.append(sampled_mpid_df.copy())
    
    sampled_df = pd.concat(sampled_mpid_df_list)
    return sampled_df