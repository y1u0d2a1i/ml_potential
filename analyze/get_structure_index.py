import pandas as pd
import os


def get_materials_id_from_comment(val):
    splitted_path = val.split('/')
    id = list(filter(lambda x: 'mp-' in x, splitted_path))[0]
    return id


def get_structure_comments(path2target, filename):
    with open(os.path.join(path2target, filename), mode='r') as f:
        l_strip = [s.strip() for s in f.readlines()]
    
    comments = list(filter(lambda x: 'comment' in x, l_strip))
    return comments


def get_structure_idx(path2target):
    """構造のIDとindexを紐付けるDFを作成

    Args:
        path2target (str): outputfileまでのpath

    Returns:
        test_structure_idx: テスト構造のmaterial-idとidxのdf
        train_structure_idx: 訓練構造のmaterial-idとidxのdf
    """
    all_data = get_structure_comments(
        path2target=path2target,
        filename='input.data'
        )
    test_data = get_structure_comments(
        path2target=path2target,
        filename='test.data'
    )
    train_data = get_structure_comments(
        path2target=path2target,
        filename='train.data'
    )
    
    all_df = pd.DataFrame(data=all_data, columns=['comment'])
    all_df = all_df.reset_index()
    all_df = all_df.rename(columns={'index': 'structure_idx'})
    test_df = pd.DataFrame(data=test_data, columns=['comment'])
    train_df = pd.DataFrame(data=train_data, columns=['comment'])
    
    # commentをkeyにしてmergeする
    test_structure_idx = pd.merge(all_df, test_df, on='comment', how='right')
    train_structure_idx = pd.merge(all_df, train_df, on='comment', how='right')
    
    test_structure_idx['materials_id'] = test_structure_idx['comment'].map(get_materials_id_from_comment)
    train_structure_idx['materials_id'] = train_structure_idx['comment'].map(get_materials_id_from_comment)
    return test_structure_idx, train_structure_idx