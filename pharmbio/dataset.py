import polars as pl
from typing import Union, List

DB_URI = "postgresql://pharmbio_readonly:readonly@imagedb-pg-postgresql.services.svc.cluster.local/imagedb"


def get_projects_list(lookup: str = None):
    query = """
        SELECT project
        FROM image_analyses_per_plate
        GROUP BY project
        ORDER BY project 
        """
    project_list = pl.read_database(query, DB_URI).to_dict(as_series=False)["project"]
    project_list = list(filter(None, project_list))
    if lookup is not None:
        lookup = lookup.lower()
        project_list = [s for s in project_list if lookup in s.lower()]
    return project_list


class ExperimentData:
    def __init__(
        self,
        name: str,
        drop_replication: Union[str, List[int]] = "Auto",
        keep_replication: Union[str, List[int]] = "None",
    ) -> None:
        # Query database and store result in Polars dataframe
        query = f"""
                SELECT *
                FROM image_analyses_per_plate
                WHERE project ILIKE '%%{name}%%'
                AND meta->>'type' = 'cp-qc'
                AND analysis_date IS NOT NULL
                ORDER BY plate_barcode 
                """

        qc_df = pl.read_database(query, DB_URI)
        data_dict = (
            qc_df.select(["project", "plate_barcode"])
            .groupby("project")
            .agg(pl.col("plate_barcode"))
            .to_dicts()
        )

        unique_project_count = qc_df.unique("project").height
        if unique_project_count == 0:
            message = f"Quering the db for {name} returned nothing."
        elif unique_project_count > 1:
            message = f"Quering the db for {name} found {unique_project_count} studies: {qc_df.unique('project')['project'].to_list()}"
        else:
            message = f"Quering the db for {name} found {unique_project_count} study: {qc_df.unique('project')['project'].to_list()}"

        print(f"{message}\n{'_'*50}")
        if unique_project_count != 0:
            self._pretty_print(data_dict)
        print("_" * 50)

        grouped_replicates = qc_df.groupby("plate_barcode")
        for plate_name, group in grouped_replicates:
            if len(group) > 1:
                print(
                    f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with analysis_id of {sorted(group['analysis_id'].to_list())}"
                )
        if qc_df.filter(pl.col("plate_barcode").is_duplicated()).is_empty():
            print("No replicated analysis has been found!")

        if drop_replication == "Auto" and keep_replication == "None":
            # keeping the highest analysis_id value of replicated rows
            qc_df = (
                qc_df.sort("analysis_id", descending=True)
                .unique("plate_barcode", keep="first")
                .sort("analysis_id")
            )
        elif isinstance(drop_replication, list):
            # drop rows by analysis_id
            qc_df = qc_df.filter(~pl.col("analysis_id").is_in(drop_replication))
        elif isinstance(keep_replication, list):
            # drop rows by analysis_id
            qc_df = qc_df.filter(pl.col("analysis_id").is_in(keep_replication))

        self.df_qc = qc_df

    def _pretty_print(self, data_list):
        for i, study in enumerate(data_list, start=1):
            print(i)
            for value in study.values():
                print("\t" + str(value))
