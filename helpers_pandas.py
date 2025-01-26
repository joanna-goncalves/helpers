import os
from typing import Dict

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, MetaData


def dataframes_to_excel(
        dataframes: Dict[str, pd.DataFrame], excel_full_path: str
) -> None:
    """
    Export DataFrames to an Excel file from a dict like keys=sheet names and values=DataFrame
    :param dataframes: DataFrames as Dict[sheet_name, data]
    :param excel_full_path: full path of the Excel File
    :return: None
    """
    os.makedirs(os.path.dirname(excel_full_path), exist_ok=True)

    with pd.ExcelWriter(excel_full_path) as writer:
        for sheet, df in dataframes.items():
            if isinstance(df.columns, pd.MultiIndex):
                df.to_excel(writer, sheet_name=sheet, merge_cells=False)
            elif df.index.dtype == np.int64 and df.index.nlevels == 1:
                df.to_excel(writer, sheet_name=sheet, merge_cells=False, index=False)
            else:
                df.to_excel(writer, sheet_name=sheet, merge_cells=False, index=True)


def dataframes_to_db(
        dataframes: Dict[str, pd.DataFrame],
        db_path: str,
        drop_all_tables: bool = False,
        append_data: bool = False,
):
    """
    Create a database from a dict like keys=sheet names and values=DataFrame
    If the SQLite database already exists, current data (before this new insertion) could be kept or erased
    :param dataframes: DataFrames as Dict(sheet_name, Data)
    :param db_path: full database path
    :param drop_all_tables: if true, all tables will be deleted
    :param append_data: if True, data will be added to the current table. If False, current data will be erased before the insertion
    :return: None
    """
    path, _ = os.path.split(db_path)
    os.makedirs(path, exist_ok=True)

    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    con = engine.connect()
    meta = MetaData()

    if drop_all_tables:
        meta.drop_all(con)

    if append_data:
        if_exists = "append"
    else:
        if_exists = "replace"

    for sh, df in dataframes.items():
        df.to_sql(name=sh, con=con, if_exists=if_exists, index=False)