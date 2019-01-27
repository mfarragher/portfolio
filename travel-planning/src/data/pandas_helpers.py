import pandas as pd


def index_matcher(left_lookup_vals_series, right_df, return_cols,
                  left_right_on_dict, concat_matches=False):
    """
    Lookup the values of a series against the column(s) of another dataframe.

    Inspired by Excel's INDEX-MATCH functionality.

    If a value is looked up and not found in the `right_df`, then the `return_cols`
    will have NaN values.

    Required argument(s):
    `left_lookup_vals_series`:  pd.Series of values to look up in `right_df`
    `right_df`:                 pd.DataFrame that contains columns to search for lookup
    `return_cols`:              list of columns to search in `right_df`
    `left_right_on_dict`:       dict of one key–value pair for joining left & right objects:
                                    {`left_lookup_vals_series` col: `right_df` col}
    Optional argument(s):
    `concat_matches`:           True to return `left_lookup_val_series` to col matches
                                    (Default value is False) 

    Returns:
    pd.DataFrame where:
        - Columns are `return_cols` (and `left_lookup_vals_series` as first col
          if `concat_matches`)
        - Indices are `left_lookup_vals_series` indices
        - Values are the lookup matches
    """
    # Retrieve 'left series' col and `right_df` col for doing merge
    left_on_col = list(left_right_on_dict.keys())[0]  # first key of dict
    right_on_col = list(left_right_on_dict.values())[0]  # first value of dict

    # Create list of columns:
    right_cols_subset = [right_on_col]  # 'on' col as first item
    right_cols_subset.extend(return_cols)  # add return_cols to list

    # Create initial dataframe of lookup
    # Notes:
    # - `left_lookup_values_series` is passed to DataFrame so that merge can be used
    # - The 'left_on' and 'right_on' cols are used for join and dropped
    matches_df = (pd.DataFrame(left_lookup_vals_series)
                  .merge(right_df[right_cols_subset], how='left',
                         left_on=left_on_col, right_on=right_on_col)
                  .drop(columns=[left_on_col, right_on_col]))

    # Dataframe has `return_cols` for cols & `left_lookup_vals_series` indices at this point

    # Ensure that returned dataframe retains the indices of 'left series'
    indices = left_lookup_vals_series.index
    matches_df.index = indices

    if concat_matches:
        # [-left_lookup_col-] + [-matches_df_cols-]
        return pd.concat([left_lookup_vals_series, matches_df], axis='columns')
    else:
        return matches_df
