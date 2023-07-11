import polars as pl
from typing import Union, List

DB_URI = 'postgresql://pharmbio_readonly:readonly@imagedb-pg-postgresql.services.svc.cluster.local/imagedb'

def get_projects_list(lookup: str = None):
    query = """
        SELECT project
        FROM image_analyses_per_plate
        GROUP BY project
        ORDER BY project 
        """
    project_list = pl.read_database(query, DB_URI).to_dict(as_series=False)['project']
    project_list = [item for item in project_list if item is not None]
    if lookup is None:
        return project_list
    lookup = lookup.lower()
    return [s for s in project_list if lookup in s.lower()]


class ExperimentData:
    def __init__(self, Name: str, drop_replication: Union[str, List[int]] = 'Auto', keep_replication: Union[str, List[int]] = 'None' ) -> None:
        query = f"""
                SELECT *
                FROM image_analyses_per_plate
                WHERE project ILIKE '%%{Name}%%'
                AND meta->>'type' = 'cp-qc'
                AND analysis_date IS NOT NULL
                ORDER BY plate_barcode 
                """
        print(f'Quering the db for {Name}')
        # Query database and store result in Polars dataframe
        qc_df = pl.read_database(query, DB_URI)
        # Check for duplicates
        duplicates = qc_df.filter(pl.col('plate_barcode').is_duplicated())

        if not duplicates.is_empty():
            # Group the duplicated data by 'plate_barcode' and count the occurrences
            grouped_duplicates = duplicates.groupby('plate_barcode')
            for plate_name, group in grouped_duplicates:
                print(f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with analysis_id of {sorted(group['analysis_id'].to_list())}")
        else:
            print("No replicted analysis has been found!")

        if drop_replication == 'Auto' and keep_replication == 'None':
            # keeping the highet analysis_id value of replicated rows
            qc_df = qc_df.sort("analysis_id", descending=True).unique('plate_barcode', keep='first').sort("analysis_id")
        elif drop_replication == 'None':
            pass
        elif isinstance(drop_replication, list):
            # drop rows by analysis_id
            qc_df = qc_df.filter(~pl.col('analysis_id').is_in(drop_replication))
        elif isinstance(keep_replication, list):
            # drop rows by analysis_id
            qc_df = qc_df.filter(pl.col('analysis_id').is_in(keep_replication))

        self.df_qc = qc_df
    