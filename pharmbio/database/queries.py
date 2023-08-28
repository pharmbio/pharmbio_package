# ------------------- This is to query over experiment name ------------------ #
def experiment_name_sql_query(experiment_name, table_name_on_db):
    return f"""
            SELECT {experiment_name}
            FROM {table_name_on_db}
            GROUP BY {experiment_name}
            ORDER BY {experiment_name}
            """


# ------------------ This is to get the experiment metadata ------------------ #
def experiment_metadata_sql_query(name, db_schema, experiment_type):
    return f"""
            SELECT *
            FROM {db_schema['EXPERIMENT_METADATA_TABLE_NAME_ON_DB']}
            WHERE {db_schema['EXPERIMENT_NAME_COLUMN']} ILIKE '%%{name}%%'
            AND meta->>'type' = '{experiment_type}'
            AND {db_schema['EXPERIMENT_ANALYSIS_DATE_COLUMN']} IS NOT NULL
            ORDER BY {db_schema['EXPERIMENT_PLATE_BARCODE_COLUMN']}, {db_schema['EXPERIMENT_PLATE_ACQID_COLUMN']}, {db_schema['EXPERIMENT_ANALYSIS_ID_COLUMN']}
            """
