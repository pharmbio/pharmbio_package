import polars as pl
from ..config import DB_URI, DATABASE_SCHEMA
from ..database.queries import experiment_name_sql_query
import json
from .image_quality import get_image_quality_ref, get_image_quality_data
from ..data_processing.quality_control import (
    get_qc_module,
    get_qc_data_dict,
    flag_outlier_images,
)
from .cell_morphology import (
    get_cell_morphology_ref,
    get_cell_morphology_data,
    get_comp_outlier_info,
    get_outlier_df,
)
from ..visualization import plots
from typing import Union, Literal, Tuple, Set, List, Dict
from ..config import COLORS


def get_projects_list(lookup: str = None):
    """
    Retrieves a list of projects.

    Args:
        lookup (str, optional): A string to filter the project list. Defaults to None.

    Returns:
        list: A list of project names.

    Example:
        ```python
        project_list = get_projects_list()
        print(project_list)
        # Output: ['Project A', 'Project B', 'Project C']

        filtered_list = get_projects_list(lookup='a')
        print(filtered_list)
        # Output: ['Project A']
        ```
    """

    query = experiment_name_sql_query(
        DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"],
        DATABASE_SCHEMA["EXPERIMENT_METADATA_TABLE_NAME_ON_DB"],
    )
    project_list = pl.read_database(query, DB_URI).to_dict(as_series=False)[
        DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"]
    ]

    project_list = list(filter(None, project_list))
    if lookup is not None:
        lookup = lookup.lower()
        project_list = [s for s in project_list if lookup in s.lower()]
    return project_list


class Experiment:
    """
    Represents an experiment with various data and functionality.

    Args:
        json_file: The path to a JSON file containing experiment data.

    Attributes:
        image_quality_data: The image quality data for the experiment.
        flagged_image_quality_data: The flagged image quality data for the experiment.
        cell_morphology_data: The cell morphology data for the experiment.
        compound_batch_ids: The list of compound batch IDs for the experiment.
        compound_outlier_info: The outlier information for the experiment's flagged image quality data.
        outlier_dataframe: The DataFrame containing outlier information for the experiment's flagged image quality data.
    """
    def __init__(self, json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
            self.__dict__.update(data)
        self.image_quality_data = self.get_image_quality_data()
        self.flagged_image_quality_data = self.flag_outlier_images()
        self.cell_morphology_data = self.get_cell_morphology_data()
        self.compound_batch_ids = (
            self.cell_morphology_data.select("batch_id")
            .unique("batch_id")
            .to_series()
            .to_list()
        )
        self.compound_outlier_info = get_comp_outlier_info(
            flagged_df=self.flagged_image_quality_data
        )
        self.outlier_dataframe = get_outlier_df(
            flagged_qc_df=self.flagged_image_quality_data,
            with_compound_info=self.__dict__.get("with_compound_info", False),
        )

    def get_image_quality_reference_data(self):
        return get_image_quality_ref(
            name=self.experiment_name,
            drop_replication=self.__dict__.get("drop_replication", "Auto"),
            keep_replication=self.__dict__.get("keep_replication", "None"),
            filter=self.__dict__.get("filter", None),
        )

    def get_image_quality_data(self):
        return get_image_quality_data(
            self.get_image_quality_reference_data(),
            force_merging_columns=self.__dict__.get("force_merging_columns", False),
        )

    def get_cell_morphology_reference_data(self):
        return get_cell_morphology_ref(
            name=self.experiment_name,
            filter=self.__dict__.get("filter_cp", None),
        )

    def get_cell_morphology_data(self):
        return get_cell_morphology_data(
            cell_morphology_ref_df=self.get_cell_morphology_reference_data(),
            flagged_qc_df=self.flagged_image_quality_data,
            site_threshold=self.__dict__.get("site_threshold", 6),
            compound_threshold=self.__dict__.get("compound_threshold", 0.7),
            aggregation_level=self.__dict__.get("aggregation_level", "cell"),
            aggregation_method=self.__dict__.get("aggregation_method", None),
            path_to_save=self.__dict__.get("path_to_save", "data"),
            use_gpu=self.__dict__.get("use_gpu", False),
            save_plate_separately=self.__dict__.get("save_plate_separately", False),
        )

    def get_image_guality_modules(self):
        return get_qc_module(qc_data=self.image_quality_data)

    def get_image_guality_data_dict(self):
        return get_qc_data_dict(
            qc_data=self.image_quality_data,
            module_to_keep=self.__dict__.get("module_to_keep", None),
            module_to_drop=self.__dict__.get("module_to_drop", None),
        )

    def flag_outlier_images(self):
        return flag_outlier_images(
            qc_data=self.image_quality_data,
            module_to_keep=self.__dict__.get("module_to_keep", None),
            module_to_drop=self.__dict__.get("module_to_drop", None),
            method=self.__dict__.get("method", "SD"),
            IQR_normalization=eval(self.__dict__.get("IQR_normalization", "True")),
            normalization=self.__dict__.get("normalization", "zscore"),
            sd_step_dict=self.__dict__.get("sd_step_dict", None),
            default_sd_step=tuple(self.__dict__.get("default_sd_step"))
            if self.__dict__.get("default_sd_step", None)
            else (-4.5, 4.5),
            quantile_limit=self.__dict__.get("quantile_limit", 0.25),
            multiplier=self.__dict__.get("quantile_limit", 1.5),
        )

    def plate_heatmap(
        self,
        plate_names: List[str] = None,
        subplot_num_columns: int = 2,
        plot_size: int = 400,
        measurement: str = "Count_nuclei",
        plate_well_columns: Dict[str, str] = None,
    ):
        plots.plate_heatmap(
            df=self.image_quality_data,
            plate_names=plate_names,
            subplot_num_columns=subplot_num_columns,
            plot_size=plot_size,
            measurement=measurement,
            plate_well_columns=plate_well_columns,
        )

    def well_outlier_heatmap(self):
        plots.plate_heatmap(self.outlier_dataframe, measurement="outlier_num")

    def quality_module_lineplot(
        self,
        qc_module_to_plot: Set[str] = None,
        title: str = "Unnamed",
        plot_size: int = 1400,
        normalization: bool = True,
        normalization_method: Literal["zscore", "minmax"] = "zscore",
        y_axis_range: Tuple = (-5, 5),
        colors: List[str] = COLORS,
    ):
        plots.quality_module_lineplot(
            df=self.image_quality_data,
            qc_module_to_plot=qc_module_to_plot,
            title=title,
            plot_size=plot_size,
            normalization=normalization,
            normalization_method=normalization_method,
            y_axis_range=y_axis_range,
            colors=colors,
        )

    def print_setting(self):
        keys_to_exclude = {
            "image_quality_data",
            "cell_morphology_data",
            "flagged_image_quality_data",
            "compound_batch_ids",
            "compound_outlier_info",
            "outlier_dataframe",
        }
        filtered_dict = {
            k: v for k, v in self.__dict__.items() if k not in keys_to_exclude
        }
        print(json.dumps(filtered_dict, indent=4))
