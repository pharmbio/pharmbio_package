import polars as pl
from pharmbio import config as cfg
from pharmbio.database.queries import (
    experiment_metadata_sql_query,
)

def get_cell_morphology_ref(
    name: str,
    filter: dict = None,
):
    query = experiment_metadata_sql_query(
        name,
        cfg.EXPERIMENT_METADATA_TABLE_NAME_ON_DB,
        cfg.EXPERIMENT_NAME_COLUMN,
        cfg.EXPERIMENT_PLATE_BARCODE_COLUMN,
        cfg.EXPERIMENT_ANALYSIS_DATE_COLUMN,
        cfg.EXPERIMENT_PLATE_ACQID_COLUMN,
        cfg.EXPERIMENT_ANALYSIS_ID_COLUMN,
        cfg.CELL_MORPHOLOGY_METADATA_TYPE,
    )
    df = pl.read_database(query, cfg.DB_URI)

    if filter is None:
        return df
    conditions = []
    # Iterate over each key-value pair in the filter dictionary
    for key, values in filter.items():
        # Create an OR condition for each value associated with a key
        key_conditions = [pl.col(key).str.contains(val) for val in values]
        combined_key_condition = key_conditions[0]
        for condition in key_conditions[1:]:
            combined_key_condition = combined_key_condition | condition
        conditions.append(combined_key_condition)
    # Combine all conditions with AND
    final_condition = conditions[0]
    for condition in conditions[1:]:
        final_condition = final_condition & condition
    # Apply the condition to the DataFrame
    return df.filter(final_condition)