from __future__ import annotations

import pandas as pd


def step_02_clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    rows_with_missing_values = dataframe.index[dataframe.isna().any(axis=1)].tolist()
    dataframe_without_missing_values = dataframe.drop(index=rows_with_missing_values)
    numeric_dataframe = dataframe_without_missing_values.apply(pd.to_numeric, errors="coerce")
    rows_with_non_numeric_values = dataframe_without_missing_values.index[
        numeric_dataframe.isna().any(axis=1)
    ].tolist()
    dataframe_with_numeric_values_only = numeric_dataframe.drop(index=rows_with_non_numeric_values)
    rows_with_negative_values = dataframe_with_numeric_values_only.index[
        (dataframe_with_numeric_values_only < 0).any(axis=1)
    ].tolist()
    cleaned_dataframe = dataframe_with_numeric_values_only.drop(
        index=rows_with_negative_values
    ).reset_index(drop=True)

    print()
    print("------------------------------------------------------------")
    print("Data cleaning statistics")
    print()
    if rows_with_missing_values:
        print(f"Removed rows with missing values: {rows_with_missing_values}")
    else:
        print("Removed rows with missing values: none")
    if rows_with_non_numeric_values:
        print(f"Removed rows with non-numeric values: {rows_with_non_numeric_values}")
    else:
        print("Removed rows with non-numeric values: none")
    if rows_with_negative_values:
        print(f"Removed rows with negative values: {rows_with_negative_values}")
    else:
        print("Removed rows with negative values: none")
    print(f"Rows remaining after cleaning: {len(cleaned_dataframe)}")

    return cleaned_dataframe
