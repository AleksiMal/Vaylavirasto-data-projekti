from __future__ import annotations

import pandas as pd


def step_04_engineer_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    selected_features = [
        "Pysty_kiiht",
        "Sivuheilahdus_kiiht",
        "Nyökkimis_kiiht",
    ]
    engineered_dataframe = dataframe.loc[:, selected_features].copy()

    print()
    print("------------------------------------------------------------")
    print("The data has been prepared for feature engineering.")
    print()
    print(engineered_dataframe.head(5).to_string())

    return engineered_dataframe
