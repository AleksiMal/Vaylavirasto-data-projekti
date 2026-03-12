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

After the validation output, the function validates and filters the data to the selected ML feature columns:

- `Pysty_kiiht`
- `Sivuheilahdus_kiiht`
- `Nyökkimis_kiiht`
- `Yhdistetty_kiiht_rms`

At least one of the required worksheets must contain all four selected ML feature columns. If neither required worksheet contains the complete feature set, the function raises an error.

The original larger worksheet data is not kept after filtering. Only the filtered dataset is retained in memory and returned from the function.

Finally, the function prints a five-row table preview of the filtered dataset.
