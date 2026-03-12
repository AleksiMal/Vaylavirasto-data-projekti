# README


## 1.1 How to run

Run the program from the `MLmodel` directory:

```bash
python ml_pipeline.py "Paallystettyjen_teiden_lahtotiedot_ominaisuus_kuntotiedot_100m_L145695.xlsx"
```

```bash
python ml_pipeline.py "Data/Paallystettyjen_teiden_lahtotiedot_ominaisuus_kuntotiedot_100m_L145695.xlsx"
```

The input must be an Excel file name with the extension `.xlsx` or `.xlsm`.

The Excel file must be located in the repository root `Data` directory. Supported input formats are a plain file name or `Data/<file name>`. Full paths and other relative paths are not supported.

## 2.1 step_01_load_data()

The `step_01_load_data()` function loads the configured Excel worksheets using worksheet-specific header row settings. If any required worksheet is missing or does not contain data rows, the function raises an error.

It first prints the first data row in the format `Worksheet | Column: value` so the loaded worksheet content can be validated before further processing.

After the validation output, the function validates the `Raportti 10m MALLI` worksheet and filters its data to the selected ML feature columns:

- `Pysty_kiiht`
- `Sivuheilahdus_kiiht`
- `Nyökkimis_kiiht`
- `Yhdistetty_kiiht_rms`

Both required worksheets must exist in the Excel file:

- `Raportti 100m`
- `Raportti 10m MALLI`

The `Raportti 10m MALLI` worksheet must contain all four selected ML feature columns. If any of these columns are missing, the function raises an error.

The original larger worksheet data is not kept after filtering. Only the filtered dataset from the `Raportti 10m MALLI` worksheet is retained in memory and returned from the function.

Finally, the function prints a five-row table preview of the filtered dataset.

## 2.2 step_02_clean_data()

The `step_02_clean_data()` function receives the filtered `DataFrame` returned by `step_01_load_data()` and removes rows that are not suitable for further processing.

It first finds all rows that contain at least one missing value and removes them from the dataset.

After that, it checks the remaining rows for non-numeric values in any column and removes those rows as well.

Finally, it checks the rows that still remain for negative values in any column and removes those rows as well.

The function then prints data cleaning statistics, including:

- the index values of removed rows with missing values
- the index values of removed rows with non-numeric values
- the index values of removed rows with negative values
- the number of rows remaining after cleaning

Finally, the function returns the cleaned `DataFrame` with its index reset.
