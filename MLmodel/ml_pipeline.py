from __future__ import annotations

import argparse
from pathlib import Path

from src.data_cleaning import step_02_clean_data
from src.feature_engineering import step_04_engineer_features
from src.data_loading import step_01_load_data


DEFAULT_DATA_FILE_PATH = (
     Path(__file__).resolve().parent.parent
     / "Data"
     / "Paallystettyjen_teiden_lahtotiedot_ominaisuus_kuntotiedot_100m_L145695.xlsx"
 )


def resolve_file_path(file_path: Path) -> Path:
    if file_path == DEFAULT_DATA_FILE_PATH:
        return file_path

    if file_path.parent == Path("."):
        return DEFAULT_DATA_FILE_PATH.parent / file_path.name

    if file_path.parent == Path("Data"):
        return DEFAULT_DATA_FILE_PATH.parent / file_path.name

    if file_path.parent == Path("data"):
        return DEFAULT_DATA_FILE_PATH.parent / file_path.name

    if file_path.parent != Path("."):
        raise ValueError(
            "Only a file name or Data/<file name> is supported. Place the Excel file in the repository Data directory."
        )

    return DEFAULT_DATA_FILE_PATH.parent / file_path.name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Loads an Excel file from the repository Data directory and prints the column names and the first data row."
    )
    parser.add_argument(
        "file_path",
        nargs="?",
        type=Path,
        default=DEFAULT_DATA_FILE_PATH,
        help="Excel file name located in the repository Data directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = resolve_file_path(args.file_path)
    print()
    print("=== ML Pipeline Started ===")
    print()
    print("------------------------------------------------------------")
    filtered_dataframe = step_01_load_data(file_path)
    cleaned_dataframe = step_02_clean_data(filtered_dataframe)
    if cleaned_dataframe.empty:
        raise ValueError(
            "Data cleaning removed all rows. No data remains for further processing."
        )
    engineered_dataframe = step_04_engineer_features(cleaned_dataframe)
    print()
    print("------------------------------------------------------------")
    print()
    print("=== ML Pipeline Finished ===")
    print()


if __name__ == "__main__":
    main()
