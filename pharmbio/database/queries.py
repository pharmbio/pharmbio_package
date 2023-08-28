# ------------------- This is to query over experiment name ------------------ #
def experiment_name_sql_query(
    experiment_name,
    table_name_on_db
    ):
    return f"""
            SELECT {experiment_name}
            FROM {table_name_on_db}
            GROUP BY {experiment_name}
            ORDER BY {experiment_name}
            """


# ------------------ This is to get the experiment metadata ------------------ #
def experiment_metadata_sql_query(
    name,
    table_name_on_db,
    experiment_name,
    plate_barcode,
    analysis_date,
    plate_acq_id,
    analysis_id,
    data_type
):
    return f"""
            SELECT *
            FROM {table_name_on_db}
            WHERE {experiment_name} ILIKE '%%{name}%%'
            AND meta->>'type' = {data_type}
            AND {analysis_date} IS NOT NULL
            ORDER BY {plate_barcode}, {plate_acq_id}, {analysis_id}
            """
