from __future__ import annotations

from pathlib import Path

import pandas as pd


def step_01_load_data(file_path: Path) -> dict[str, pd.DataFrame]:
    validated_path = Path(file_path)

    if not validated_path.exists():
        raise FileNotFoundError(f"File not found: {validated_path}")

    if validated_path.suffix.lower() not in {".xlsx", ".xlsm"}:
        raise ValueError(
            "Invalid file type. Please provide an Excel file with the extension .xlsx or .xlsm."
        )

    sheet_headers = {
        "Raportti 100m": 1,
        "Raportti 10m MALLI": 0,
    }
    selected_features = [
        "Pysty_kiiht",
        "Sivuheilahdus_kiiht",
        "Nyökkimis_kiiht",
        "Yhdistetty_kiiht_rms",
    ]
    filtered_dataframes: dict[str, pd.DataFrame] = {}
    empty_sheet_names: list[str] = []
    sheets_missing_selected_features: dict[str, list[str]] = {}

    with pd.ExcelFile(validated_path) as excel_file:
        available_sheet_names = excel_file.sheet_names
    missing_sheet_names = [
        sheet_name for sheet_name in sheet_headers if sheet_name not in available_sheet_names
    ]

    if missing_sheet_names:
        raise ValueError(
            "The Excel file is missing required worksheet(s): "
            f"{', '.join(missing_sheet_names)}. "
            f"Available worksheets: {', '.join(available_sheet_names)}"
        )

    print("Reading selected worksheets. Please wait...")

    for sheet_name, header_row in sheet_headers.items():
        dataframe = pd.read_excel(validated_path, header=header_row, sheet_name=sheet_name)
        if dataframe.empty:
            empty_sheet_names.append(sheet_name)
            continue

        first_row = dataframe.iloc[0]
        for column_name, value in first_row.items():
            print(f"{sheet_name} | {column_name}: {value}")

        missing_features = [feature for feature in selected_features if feature not in dataframe.columns]
        if missing_features:
            sheets_missing_selected_features[sheet_name] = missing_features
            del dataframe
            continue

        filtered_dataframe = dataframe.loc[:, selected_features].copy()
        filtered_dataframes[sheet_name] = filtered_dataframe
        del dataframe

    if empty_sheet_names:
        raise ValueError(
            "The following required worksheets do not contain data rows: "
            f"{', '.join(empty_sheet_names)}"
        )

    if not filtered_dataframes:
        if sheets_missing_selected_features:
            missing_feature_details = "; ".join(
                f"{sheet_name}: missing {', '.join(missing_features)}"
                for sheet_name, missing_features in sheets_missing_selected_features.items()
            )
            raise ValueError(
                "Neither required worksheet contains all selected ML feature columns. "
                f"Details: {missing_feature_details}. "
                f"Selected ML features: {', '.join(selected_features)}"
            )

        raise ValueError(
            "The required worksheets did not produce any usable ML feature data."
        )

    print("------------------------------------------------------------")
    print("The data has been filtered to the selected ML features.")
    for sheet_name, dataframe in filtered_dataframes.items():
        print()
        print(dataframe.head(5).to_string())

    return filtered_dataframes
