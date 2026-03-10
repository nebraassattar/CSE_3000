import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    exclude = {'anon_id', 'name', 'id'}
    quasi_identifiers = [
        col for col in anon_df.columns
        if col in aux_df.columns and col.lower() not in exclude
    ]
    merged = anon_df.merge(aux_df, on=quasi_identifiers, how='inner')
    name_col = next((c for c in aux_df.columns if c.lower() == 'name'), None)
    id_col = next((c for c in anon_df.columns if c.lower() == 'anon_id'), None)
    match_counts = merged.groupby(id_col)[name_col].transform('nunique')
    unique_matches = merged[match_counts == 1][[id_col, name_col]].drop_duplicates()
    unique_matches.columns = ['anon_id', 'matched_name']
    return unique_matches.reset_index(drop=True)
    raise NotImplementedError


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    total = len(anon_df)
    if total == 0:
        return 0.0
    reidentified = len(matches_df)
    return reidentified / total
    raise NotImplementedError
