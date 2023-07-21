import os
import polars as pl
from typing import Union, Tuple, Literal, Set, List, Dict
from .qc import flag_outliers, get_qc_module, get_qc_data_dict, get_channels
from .vs import qc_lineplot, plate_heatmap, COLORS

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


def get_qc_info(
    name: str,
    drop_replication: Union[str, List[int]] = "Auto",
    keep_replication: Union[str, List[int]] = "None",
    filter: dict = None,
):  # sourcery skip: low-code-quality
    # Query database and store result in Polars dataframe
    query = f"""
            SELECT *
            FROM image_analyses_per_plate
            WHERE project ILIKE '%%{name}%%'
            AND meta->>'type' = 'cp-qc'
            AND analysis_date IS NOT NULL
            ORDER BY plate_barcode 
            """
    qc_info_df = pl.read_database(query, DB_URI)
    data_dict = (
        qc_info_df.select(["project", "plate_barcode"])
        .groupby("project")
        .agg(pl.col("plate_barcode"))
        .to_dicts()
    )
    unique_project_count = qc_info_df.unique("project").height
    if unique_project_count == 0:
        message = f"Quering the db for {name} returned nothing."
    elif unique_project_count > 1:
        message = f"Quering the db for {name} found {unique_project_count} studies: {qc_info_df.unique('project')['project'].to_list()}"
    else:
        message = f"Quering the db for {name} found {unique_project_count} study: {qc_info_df.unique('project')['project'].to_list()}"
    print(f"{message}\n{'_'*50}")
    if unique_project_count != 0:
        for i, study in enumerate(data_dict, start=1):
            print(i)
            for value in study.values():
                print("\t" + str(value))
    print("_" * 50)
    grouped_replicates = qc_info_df.groupby("plate_barcode")
    for plate_name, group in grouped_replicates:
        if len(group) > 1:
            print(
                f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with analysis_id of {sorted(group['analysis_id'].to_list())}"
            )
    if qc_info_df.filter(pl.col("plate_barcode").is_duplicated()).is_empty():
        print("No replicated analysis has been found!")
    if drop_replication == "Auto" and keep_replication == "None":
        # keeping the highest analysis_id value of replicated rows
        qc_info_df = (
            qc_info_df.sort("analysis_id", descending=True)
            .unique("plate_barcode", keep="first")
            .sort("analysis_id")
        )
    elif isinstance(drop_replication, list):
        # drop rows by analysis_id
        qc_info_df = qc_info_df.filter(~pl.col("analysis_id").is_in(drop_replication))
    elif isinstance(keep_replication, list):
        # drop rows by analysis_id
        qc_info_df = qc_info_df.filter(pl.col("analysis_id").is_in(keep_replication))

    if filter is None:
        return qc_info_df
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
    return qc_info_df.filter(final_condition)


def _get_file_extension(filename):
    """Helper function to get file extension"""
    possible_extensions = [".parquet", ".csv", ".tsv"]
    for ext in possible_extensions:
        full_filename = filename + ext
        if os.path.isfile(full_filename):
            return ext
    print(
        f"Warning: No file with extensions {possible_extensions} was not found for {filename}."
    )
    return None


import polars as pl


def _read_file(filename, extension):
    """Helper function to read file based on its extension"""
    if extension == ".parquet":
        df = pl.read_parquet(filename + extension)
    elif extension in [".csv", ".tsv"]:
        delimiter = "," if extension == ".csv" else "\t"
        df = pl.read_csv(filename + extension, separator=delimiter)
    else:
        return None
    # Change column type to float32 if all values are null (unless in some case it changes to str)
    for name in df.columns:
        if df[name].is_null().sum() == len(df[name]):
            df = df.with_columns(df[name].cast(pl.Float32))
    return df


def get_qc_data(
    filtered_qc_info: pl.DataFrame, force_merging_columns: Union[bool, str] = False
):
    # Add qc_file column based on 'results' and 'plate_barcode' columns
    filtered_qc_info = filtered_qc_info.with_columns(
        (pl.col("results") + "qcRAW_images_" + pl.col("plate_barcode")).alias("qc_file")
    )
    print("\n")
    # Read and process all the files in a list, skipping files not found
    dfs = []
    for row in filtered_qc_info.iter_rows(named=True):
        ext = _get_file_extension(row["qc_file"])
        if ext is not None:
            df = _read_file(row["qc_file"], ext)
            df = df.with_columns(
                pl.lit(row["plate_acq_id"]).alias("Metadata_AcqID"),
                pl.lit(row["plate_barcode"]).alias("Metadata_Barcode"),
            )
            # Cast all numerical f64 columns to f32
            for name, dtype in zip(df.columns, df.dtypes):
                if dtype == pl.Float64:
                    df = df.with_columns(pl.col(name).cast(pl.Float32))
                elif dtype == pl.Int64:
                    df = df.with_columns(pl.col(name).cast(pl.Int32))
            dfs.append(df)
            print(f"Successfully imported {df.shape}: {row['qc_file']}{ext}")

    if force_merging_columns == "keep":
        concat_method = "diagonal"  # keep all columns and fill missing values with null
    elif force_merging_columns == "drop":
        concat_method = (
            "vertical"  # merge dfs horizontally, only keeps matching columns
        )
        common_columns = set(dfs[0].columns)
        for df in dfs[1:]:
            common_columns.intersection_update(df.columns)
        dfs = [df.select(sorted(common_columns)) for df in dfs]
    else:
        # Check if all dataframes have the same shape, if not print a message
        if len({df.shape[1] for df in dfs}) > 1:
            print("\nDataframes have different shapes and cannot be stacked together!")
            return None
        concat_method = "vertical"  # standard vertical concatenation

    print(f"\n{'_'*50}\nQuality control data of {len(dfs)} plates imported!\n")
    # Concatenate all the dataframes at once and return it
    return (
        pl.concat(dfs, how=concat_method)
        .with_columns(
            (
                pl.col("Metadata_AcqID").cast(pl.Utf8)
                + "_"
                + pl.col("Metadata_Well")
                + "_"
                + pl.col("Metadata_Site").cast(pl.Utf8)
            ).alias("ImageID")
        )
        .sort(["Metadata_Barcode", "Metadata_Well", "Metadata_Site", "ImageID"])
        if dfs
        else None
    )


class ExperimentData:
    def __init__(
        self,
        name: str,
        drop_replication: Union[str, List[int]] = "Auto",
        keep_replication: Union[str, List[int]] = "None",
        force_merging_columns: Union[bool, str] = False,
        filter: dict = None,
    ) -> None:
        self.qc_info = get_qc_info(name, drop_replication, keep_replication, filter)
        self.qc_data = get_qc_data(
            self.qc_info, force_merging_columns=force_merging_columns
        )
        self.project = sorted(self.qc_info["project"].unique().to_list())
        self.project_name = self.project[0] if len(self.project) == 1 else None
        self.pipeline_name = sorted(self.qc_info["pipeline_name"].unique().to_list())
        self.analysis_date = sorted(self.qc_info["analysis_date"].unique().to_list())
        self.plate_barcode = sorted(self.qc_info["plate_barcode"].unique().to_list())
        self.plate_acq_name = sorted(self.qc_info["plate_acq_name"].unique().to_list())
        self.plate_acq_id = sorted(self.qc_info["plate_acq_id"].unique().to_list())
        self.analysis_id = sorted(self.qc_info["analysis_id"].unique().to_list())
        if self.qc_data is not None:
            self.plate_wells = (
                self.qc_data.select("Metadata_Well")
                .unique()
                .sort(by="Metadata_Well")
                .to_series()
                .to_list()
            )
            self.plate_rows = sorted(list({w[0] for w in self.plate_wells}))
            self.plate_columns = sorted(list({w[1:] for w in self.plate_wells}))
            self.qc_module = get_qc_module(self.qc_data)

    def flag_it(
        self,
        module_to_keep: Set[str] = None,
        module_to_drop: Set[str] = None,
        method: Literal["SD", "IQR"] = "SD",
        IQR_normalization: bool = True,
        normalization: Literal["zscore", "minmax"] = "zscore",
        sd_step_dict: Dict[str, Tuple[float, float]] = None,
        default_sd_step: Tuple[float, float] = (-4.5, 4.5),
        quantile_limit: float = 0.25,
        multiplier: float = 1.5,
    ):
        return flag_outliers(
            self.qc_data,
            module_to_keep,
            module_to_drop,
            method,
            IQR_normalization,
            normalization,
            sd_step_dict,
            default_sd_step,
            quantile_limit,
            multiplier,
        )

    def qc_data_dict(
        self,
        module_to_keep: Set[str] = None,
        module_to_drop: Set[str] = None,
    ):
        return get_qc_data_dict(
            self.qc_data,
            module_to_keep,
            module_to_drop,
        )

    def channels(
        self,
        qc_module_list: List[str] = None,
    ):
        d = get_channels(self.qc_data, qc_module_list)
        for module, data in d.items():
            print(module)
            print("  Channels:", data["channels"])
            if data["sub_channels"] != []:
                print("  Sub-channels:", data["sub_channels"])
            print()
        return d

    def plate_heatmap(
        self,
        plate_names: List[str] = None,
        subplot_num_columns: int = 2,
        plot_size: int = 400,
        measurement: str = "Count_nuclei",
    ):
        if not plate_names:
            plate_names = self.plate_barcode
        return plate_heatmap(
            self.qc_data,
            plate_names,
            subplot_num_columns,
            plot_size,
            measurement,
        )

    def qc_lineplot(
        self,
        qc_module_to_plot: Set[str] = None,
        title: str = None,
        plot_size: int = 1400,
        normalization: bool = True,
        normalization_method: Literal["zscore", "minmax"] = "zscore",
        y_axis_range: Tuple = (-5, 5),
        colors: List[str] = COLORS,
    ):
        if not title:
            title = self.project_name
        return qc_lineplot(
            self.qc_data,
            qc_module_to_plot,
            title,
            plot_size,
            normalization,
            normalization_method,
            y_axis_range,
            colors,
        )