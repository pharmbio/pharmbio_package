import polars as pl
import pandas as pd
from typing import Union, Literal

def normalize_df(df: Union[pl.DataFrame, pd.DataFrame], method: Literal["zscore", "minmax"] = "zscore"):
    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    methods = {
        "minmax": lambda x: (x - x.min()) / (x.max() - x.min()),
        "zscore": lambda x: (x - x.mean()) / x.std(ddof=1),
    }

    df = df.select(
        [
            (
                methods[method](df[col])
                if df[col].dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]
                else df[col]
            ).alias(col)
            for col in df.columns
        ]
    )
    return df
