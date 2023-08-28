import polars as pl
from pharmbio import config as cfg
from pharmbio.database.queries import experiment_name_sql_query


def get_projects_list(lookup: str = None):
    query = experiment_name_sql_query(
        cfg.EXPERIMENT_NAME_COLUMN, cfg.EXPERIMENT_METADATA_TABLE_NAME_ON_DB
    )
    project_list = pl.read_database(query, cfg.DB_URI).to_dict(as_series=False)[
        cfg.EXPERIMENT_NAME_COLUMN
    ]

    project_list = list(filter(None, project_list))
    if lookup is not None:
        lookup = lookup.lower()
        project_list = [s for s in project_list if lookup in s.lower()]
    return project_list
