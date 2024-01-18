## `pharmbio.dataset.experiment`

This module contains functions related to handling and querying experiment-related data in the `pharmbio` package.

### `get_projects_list()` 

Retrieves a list of project names from the database, with an optional filter to return only those projects that contain a specified substring in their names.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/experiment.py#L6)

```python
def get_projects_list(lookup: str = None) -> list:
```

#### Parameters

- `lookup` (str, optional): A string to filter the project list. If provided, the function returns

 only those projects that contain the `lookup` string in their names. The search is case-insensitive and the `lookup` string can match any part of a project name. Defaults to `None`, which returns all project names.

#### Returns

- `list`: A list of project names. If `lookup` is provided, it returns a filtered list of names that contain the `lookup` string. If `lookup` is `None`, it returns all project names.

#### Examples
1. **Retrieving All Projects:**
   To get a complete list of all projects:
   ```python
   project_list = get_projects_list()
   print(project_list)
   # Output: ['Project A', 'Project B', 'Project C', ...]
   ```

2. **Retrieving Filtered Projects:**
   To get a list of projects that include a specific substring (e.g., 'aros'):
   ```python
   filtered_list = get_projects_list(lookup='aros')
   print(filtered_list)
   # Output might include: ['AROS-CP', 'AROS-Reproducibility-MoA-Full', ...]
   ```

!!! Info

      - The function performs a case-insensitive search when the `lookup` parameter is used.
      - The search functionality can identify partial matches in project names, making it versatile for a variety of search requirements.
      - It is essential to ensure that your workspace is connected to the correct database server as outlined in the Configuration section of the documentation, as this function depends on database access.

## `pharmbio.dataset.cell_morphology`

This module contains functions related to handling and querying cell morphology data in the `pharmbio` package.

### `get_cell_morphology_ref()`

Retrieves cell morphology references from a specified database, allowing users to specify a reference name and apply optional filtering conditions to refine the search results. This function is particularly useful for extracting specific cell morphology data based on user-defined criteria.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L22)

```python
def get_cell_morphology_ref(
    name: str,
    filter: Optional[Dict[str, str]] = None,
) -> pl.DataFrame:
```

#### Parameters

- `name` (str): The name of the cell morphology reference to be retrieved. This is a mandatory parameter.
- `filter` (dict, optional): A dictionary specifying filter conditions for the query. Each key represents a column name, and its corresponding value is a list of strings to match in that column. The filter uses logical OR for values under the same key and logical AND across different keys. Defaults to `None`, indicating no filter will be applied.

#### Returns

- `pl.DataFrame`: A pandas-like DataFrame containing the filtered cell morphology references. The DataFrame's structure depends on the database schema and the applied filter.

#### Examples

Retrieve a specific cell morphology reference with optional filtering:

```python
name = "example_reference"
filter = {
    "column1": ["value_1", "value2"],  # Values combined with OR within the same key
    "column2": ["value3"]              # Different keys combined with AND
}
filtered_df = get_cell_morphology_ref(name, filter)
display(filtered_df)
```

!!! Info

     - The function constructs a SQL query using internal configuration parameters such as the database schema and cell morphology metadata type.
     - It executes the query against the database specified in the configuration, retrieving relevant data based on the provided `name` and `filter`.
     - When a filter is provided, the function applies the filter conditions iteratively to the DataFrame, allowing for complex query constructions.
     - Ensure that your workspace is properly configured for database connectivity as outlined in the Configuration section of the documentation.


### `_get_join_columns()`

Generates a list of columns to be used for joining tables based on a specified object type in cell morphology datasets. This function is a utility intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L74)

```python
def _get_join_columns(object_type: str) -> list:
```

#### Parameters

- `object_type` (str): The type of the object. Must be one of `'cells'`, `'cytoplasm'`, or `'nuclei'`. This parameter determines the set of columns relevant for the join operation in cell morphology datasets.

#### Returns

- `list`: A list of column names to join on. These columns are dynamically determined based on the `object_type`.

#### Raises

- `ValueError`: This error is raised if the `object_type` is not one of the allowed types ('cells', 'cytoplasm', 'nuclei').

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of an internal call within the module
object_type = 'cells'
join_columns = _get_join_columns(object_type)
```

!!! Info

    - The function dynamically determines the allowed object types from from `OBJECT_FILE_NAMES` object located in in `pharmbio.config` .
    - It constructs the list of join columns based on the provided `object_type`, ensuring that the resulting list is specific to the context of the object type.
    - This function is designed for internal use within the module, providing support for complex data operations involving cell morphology datasets.
    - Proper understanding of the database schema and configuration (as outlined in `pharmbio.config`) is necessary to effectively utilize this function.


### `_join_object_dataframes()`

Merges multiple object-related dataframes based on specified columns, facilitating the combination of different cell morphology datasets. This function is designed for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L114C1-L140C6)

```python
def _join_object_dataframes(dfs: Dict[str, pl.DataFrame]) -> pl.DataFrame:
```

#### Parameters

- `dfs` (Dict[str, pl.DataFrame]): A dictionary containing dataframes keyed by object type (`'cells'`, `'cytoplasm'`, `'nuclei'`). Each key corresponds to an object type and its associated dataframe.

#### Returns

- `pl.DataFrame`: The resulting dataframe after joining the specified dataframes. This dataframe combines the data from the different object types into a single unified structure.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
dataframes = {
    "cells": cells_df,
    "nuclei": nuclei_df,
    "cytoplasm": cytoplasm_df
}
joined_df = _join_object_dataframes(dataframes)
# joined_df is the combined dataframe of cells, nuclei, and cytoplasm data
```

!!! Info

     - The function performs a series of join operations on the dataframes provided in the `dfs` dictionary.
     - It uses the `_get_join_columns` function to determine the appropriate columns to join on for each object type.
     - The join operations are executed in a specific order to ensure correct alignment and integration of the data across different cell morphology datasets.
     - This function is crucial for scenarios where data from multiple cell components (cells, nuclei, cytoplasm) need to be combined for comprehensive analysis.
     - As an internal utility function, it plays a key role in facilitating complex data manipulations within the cell morphology module.

### `_rename_joined_df_columns()`

Renames specific columns in a dataframe, typically used to simplify column names after joining multiple dataframes. This function targets columns that have had additional identifiers appended to them during the join operation, such as '_cells', and removes these parts to restore the original column names. It is intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L143C1-L163C33)

```python
def _rename_joined_df_columns(df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `df` (pl.DataFrame): The dataframe whose columns are to be renamed. This dataframe is typically the result of a join operation that has appended additional identifiers to certain column names.

#### Returns

- `pl.DataFrame`: The dataframe with its specific columns renamed. This renaming process removes appended parts like '_cells', returning the dataframe to a more standard column naming convention.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
joined_df = _join_object_dataframes(dataframes)
renamed_df = _rename_joined_df_columns(joined_df)
# renamed_df now has simplified column names, removing appended parts from the join operation
```

!!! Info

     - The function focuses on a predefined set of specific columns that are known to undergo renaming during join operations.
     - It creates a mapping (rename_map) to translate from the joined column names back to the original column names.
     - This renaming is crucial for maintaining consistency and clarity in the dataframe, especially after complex join operations.
     - The function is an integral part of data preprocessing within the cell morphology module, ensuring that dataframes are kept in a standardized and easily interpretable format.


### `_add_image_cell_id_columns()`

Adds unique Image ID and Cell ID columns to a dataframe. This function is designed to enhance data identification by creating distinct identifiers for each image and cell, based on the existing metadata columns. It is used internally within the `cell_morphology` module to facilitate easier tracking and analysis of cell morphology data.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L166C1-L193C38)

```python
def _add_image_cell_id_columns(df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `df` (pl.DataFrame): The original dataframe to which the new ID columns will be added. This dataframe should contain metadata columns that are used to generate the unique identifiers.

#### Returns

- `pl.DataFrame`: The modified dataframe with two new columns: 'image_id' and 'cell_id'. These columns represent unique identifiers for each image and cell, respectively.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
original_df = ... # some dataframe with required metadata columns
df_with_ids = _add_image_cell_id_columns(original_df)
# df_with_ids now contains 'image_id' and 'cell_id' columns
```

!!! Info

     - The function constructs the 'image_id' column by concatenating several metadata columns: acquisition ID, barcode, well, and site. This concatenated string uniquely identifies each image.
     - The 'cell_id' column is created by appending the cell object number to the 'image_id', providing a unique identifier for each cell within an image.
     - These additional columns are crucial for tasks that require tracking and analysis at the level of individual images and cells.
     - The function enhances data organization and accessibility, making it easier to reference specific images or cells in complex datasets.


### `_drop_unwanted_columns()`

Drops specified columns from a dataframe if they exist. This function is used to clean and streamline the dataframe by removing unnecessary or redundant columns, enhancing data clarity and efficiency. It is intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L196C1-L219C67)

```python
def _drop_unwanted_columns(df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `df` (pl.DataFrame): The dataframe from which the specified columns are to be dropped. This dataframe may contain a variety of columns, some of which are not required for further analysis or operations.

#### Returns

- `pl.DataFrame`: The modified dataframe with specified unwanted columns removed.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
original_df = ... # some dataframe with a mix of required and unwanted columns
cleaned_df = _drop_unwanted_columns(original_df)
# cleaned_df is now free from specified unwanted columns
```

!!! Info

     - The function targets a predefined list of columns to be dropped, which are identified as unnecessary for the dataset's intended use.
     - These columns might include metadata or derived attributes that are redundant or irrelevant for specific analyses or data processing tasks.
     - By removing these columns, the function helps maintain a focused and efficient dataset, facilitating more effective data handling and analysis.
     - This process of dropping unwanted columns is a common practice in data preprocessing, especially in large datasets with complex structures.


### `_cast_metadata_type_columns()`

Ensures data type consistency for specified metadata columns within a dataframe. This function is used to standardize the data types of critical metadata columns, facilitating consistent data processing and analysis. It is intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L221C1-L242C38)

```python
def _cast_metadata_type_columns(df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `df` (pl.DataFrame): The dataframe whose metadata columns are to be cast to the correct data type. This dataframe typically contains various metadata fields essential for analysis.

#### Returns

- `pl.DataFrame`: The modified dataframe with specified metadata columns cast to the correct data type.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
original_df = ... # some dataframe with metadata columns
df_with_cast_types = _cast_metadata_type_columns(original_df)
# df_with_cast_types has metadata columns standardized to the correct data type
```

!!! Info

     - The function focuses on a set of predefined metadata columns crucial for data analysis.
     - These columns are cast to a uniform data type (UTF-8 string) to ensure consistency across the dataset.
     - Standardizing the data types of metadata columns is essential for reliable data processing, particularly when these columns are used in operations like joins, filtering, or aggregation.
     - By casting the metadata columns to a specific type, the function reduces potential issues related to data type mismatches, such as incorrect sorting or failed join operations.
     - This step is a common practice in data preprocessing to ensure that data from various sources or formats aligns correctly for subsequent analysis.


### `_reorder_dataframe_columns()`

Reorders the columns in a dataframe based on data types and specific columns. This function is designed to organize dataframe columns in a systematic manner, enhancing readability and analysis efficiency. It is intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L260C1-L280C32)

```python
def _reorder_dataframe_columns(df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `df` (pl.DataFrame): The original dataframe whose columns are to be reordered.

#### Returns

- `pl.DataFrame`: The dataframe with its columns reordered. The reordering is based on a predefined logic that categorizes columns by their data type and relevance.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
original_df = ... # some dataframe with various columns
reordered_df = _reorder_dataframe_columns(original_df)
# reordered_df has its columns systematically organized
```

!!! Info

     - The function first identifies morphology feature columns using `_get_morphology_feature_cols`.
     - It then segregates non-numeric columns and sorts them alphabetically.
     - The new column order starts with sorted non-numeric columns, followed by specific count columns (like `CELL_NUCLEI_COUNT_COLUMN` and `CELL_CYTOPLASM_COUNT_COLUMN` which are located in config settings), and finally includes the morphology feature columns.
     - This systematic reordering of columns is crucial for maintaining a consistent structure across different dataframes within the module, facilitating easier data manipulation and analysis.
     - The reorganization enhances the clarity of the dataframe, making it more intuitive to work with, especially when dealing with large and complex datasets.
     - By focusing on data types and specific columns, this function ensures that the most critical and relevant data is easily accessible and comprehensible.


### `_merge_with_plate_info()`

Merges a given object dataframe with plate information, enhancing the dataset with additional details relevant to the experimental setup. This function is designed to integrate cellular morphology features with plate layout data, crucial for analysis in cell morphology studies. It is intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L283C1-L316C83)

```python
def _merge_with_plate_info(df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `df` (pl.DataFrame): The original object dataframe containing cellular morphology features.
- `plate_layout_sql_query` (callable): A function that returns an SQL query for fetching plate layout information. This parameter is typically configured within the function.

#### Returns

- `pl.DataFrame`: The dataframe resulting from merging the original dataframe with plate layout information.

#### Examples

Usage of this function typically occurs internally within the `cell_morphology` module. Here is an example scenario of its use:

```python
# Example of internal usage within the module
object_df = ... # some dataframe with cellular morphology features
merged_df = _merge_with_plate_info(object_df)
# merged_df now contains both cellular morphology features and plate layout information
```

!!! Info

     - The function starts by extracting unique barcodes from the dataframe to identify the relevant plates.
     - It then fetches plate layout data from the database using a provided SQL query, which is tailored to include only the plates of interest based on their barcodes.
     - The object dataframe and plate layout dataframe are merged on barcode and well information, integrating detailed plate data with the cellular features.
     - This merge process is crucial for experiments where understanding the context of each plate and well is vital for accurate analysis and interpretation.
     - The function ensures that the merged dataframe is free of null values in crucial columns, such as the compound name column, to maintain data integrity and relevance.



### `get_cell_morphology_data()`

Retrieves and aggregates cell morphology data from a specified reference DataFrame, performing data processing and aggregation at various levels based on user-defined parameters. This function serves as the main entry point for handling cell morphology data in the `pharmbio` package.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/cell_morphology.py#L319)

```python
def get_cell_morphology_data(
    cell_morphology_ref_df: Union[pl.DataFrame, pd.DataFrame],
    aggregation_level: str = "cell",
    aggregation_method: Optional[Dict[str, str]] = None,
    path_to_save: str = "data",
    use_gpu: bool = False,
    save_plate_separately: bool = False
) -> pl.DataFrame:
```

#### Parameters

- `cell_morphology_ref_df` (Union[pl.DataFrame, pd.DataFrame]): The reference DataFrame containing cell morphology data.
- `aggregation_level` (str, optional): The level at which to perform data aggregation. Can be one of "cell", "site", "well", "plate", or "compound". Defaults to "cell".
- `aggregation_method` (Dict[str, str], optional): A dictionary specifying the aggregation method for each level (e.g., "mean", "median", "sum", "min", "max", "first", "last"). Defaults to None.
- `path_to_save` (str, optional): The path where the aggregated data will be saved. Defaults to "data".
- `use_gpu` (bool, optional): Flag to enable GPU acceleration. Defaults to False.
- `save_plate_separately` (bool, optional): Flag to indicate whether to save aggregated data for each plate separately. Defaults to False.

#### Returns

- `pl.DataFrame`: The aggregated cell morphology data as a DataFrame.

#### Raises

- `EnvironmentError`: Raised when GPU acceleration is requested but not available on the machine

#### Examples

To aggregate cell morphology data at the plate level:

```python
cell_morphology_ref_df = get_cell_morphology_ref("example_reference")
aggregated_df = get_cell_morphology_data(cell_morphology_ref_df, aggregation_level='plate')
display(aggregated_df)
```

!!! Info

     - This function acts as a workflow for processing cell morphology data, integrating various internal functions for data loading, joining, cleaning, and aggregation.
     - The function iterates over each plate's metadata in the reference DataFrame, processing and aggregating data according to the specified aggregation level and method.
     - It employs GPU acceleration for data aggregation if `use_gpu` is set to `True` and a compatible GPU is available, otherwise, it defaults to CPU processing.
     - If `save_plate_separately` is `True`, it saves the aggregated data for each plate as a separate file. Alternatively, it concatenates data from all plates into a single DataFrame.
     - The function handles various data processing steps, such as joining different object dataframes, renaming columns for consistency, creating unique identifiers, dropping unwanted columns, casting metadata columns to the correct type, reordering columns, and merging with plate information.
     - The final output is a comprehensive DataFrame containing aggregated cell morphology data, tailored to the specific requirements of the analysis level and method.
     - This function is key to the `pharmbio` package's capability to handle complex cell morphology datasets, providing a streamlined and efficient way to process and analyze large volumes of data.

## `pharmbio.dataset.image_quality`

This module in the `pharmbio` package is dedicated to handling and querying image quality data.

### `_get_image_quality_reference_df()`

Retrieves an image quality reference dataframe along with an associated data dictionary from the database for a given experiment. This function is essential for obtaining image quality metadata and plate barcodes pertinent to a specific experiment, providing a foundation for image quality analysis.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/image_quality.py#L23C1-L52C49)

```python
def _get_image_quality_reference_df(experiment_name: str) -> (pl.DataFrame, dict):
```

#### Parameters

- `experiment_name` (str): The name of the experiment for which image quality data is to be retrieved. This parameter is used to filter and fetch relevant data from the database.

#### Returns

- `image_quality_reference_df` (pl.DataFrame): A dataframe containing image quality metadata specific to the experiment. This dataframe includes various metrics and information relevant to assessing the quality of images.
- `data_dict` (dict): A dictionary mapping experiment names to lists of plate barcodes. This dictionary provides a quick reference to the plates associated with each experiment, facilitating further data processing or analysis.

#### Examples

To retrieve image quality data for a specific experiment:

```python
experiment_name = "example_experiment"
image_quality_ref_df, plate_barcodes_dict = _get_image_quality_reference_df(experiment_name)
# image_quality_ref_df contains image quality metadata
# plate_barcodes_dict maps experiment names to plate barcodes
```

!!! Info

     - The function constructs an SQL query using the provided `experiment_name`, the database schema, and the image quality metadata type (`IMAGE_QUALITY_METADATA_TYPE`).
     - The resulting `image_quality_reference_df` contains detailed metadata for each image in the experiment, including various quality metrics and identifiers.
     - The `data_dict` is created by grouping the DataFrame by the experiment name and aggregating plate barcodes. This dictionary is useful for quickly referencing which plates are associated with each experiment.



### `_logging_information_image_quality_ref()`

Logs detailed information about a given image quality reference dataframe, data dictionary, and experiment name. This function is primarily used for logging and debugging purposes, providing insights into the data retrieved and any anomalies or patterns observed.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/image_quality.py#L55C1-L109C59)

```python
def _logging_information_image_quality_ref(
    image_quality_reference_df: pl.DataFrame,
    image_quality_data_dict: Dict,
    experiment_name: str,
    unique_project_count: int
):
```

#### Parameters

- `image_quality_reference_df` (pl.DataFrame): A dataframe containing image quality metadata.
- `image_quality_data_dict` (Dict): A dictionary mapping experiment names to lists of plate barcodes.
- `experiment_name` (str): The name of the experiment being queried.
- `unique_project_count` (int): The number of unique studies found for the given experiment.

#### Functionality

- The function logs the number of studies found for the specified experiment name.
- It logs the details of the data dictionary, mapping experiments to plate barcodes.
- The function also identifies and logs any replicated analyses found in the dataframe, alerting to potential duplicates or redundancies in the data.

#### Examples

The function is used internally for logging purposes. For example:

```python
_logging_information_image_quality_ref(image_quality_ref_df, data_dict, "Experiment_X", unique_project_count)
# This will log information, including the number of studies found and details about plate barcodes.
```

!!! Info

     - The function begins by constructing a message based on the number of unique studies found for the experiment, providing a quick overview of the query results.  It then iterates through the `image_quality_data_dict`, logging the experiment names and corresponding lists of plate barcodes. This provides clarity on the scope and range of the data retrieved.
     - The function checks for replicated analyses within the dataframe. If duplicates are detected, it logs a warning with details about the replicated plates and their analysis IDs, which is crucial for data integrity checks.
     - In the absence of replicated analyses, a log message confirms that no duplicates were found, ensuring data uniqueness and reliability.
     - This logging function plays a critical role in data validation and error tracking, making it an essential tool for quality control and debugging in the data processing pipeline.
     - By providing detailed logs, it aids in diagnosing issues with the data or the querying process, thereby facilitating efficient troubleshooting and ensuring the accuracy of the image quality analysis.


### `get_image_quality_ref()`

Retrieves image quality reference data from the database based on the specified experiment name and optional filters. This function enables the selection and refinement of image quality data for specific experimental conditions, with capabilities to handle data replications and apply custom filters.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/image_quality.py#L112C1-L190C59)

```python
def get_image_quality_ref(
    name: str,
    drop_replication: Union[str, List[int]] = "Auto",
    keep_replication: Union[str, List[int]] = "None",
    filter: dict = None
) -> pl.DataFrame:
```

#### Parameters

- `name` (str): The name of the experiment for which to retrieve image quality reference data.
- `drop_replication` (Union[str, List[int]], optional): Specifies which replications to drop. Can be set to "Auto" (to keep the latest experiment), "None", or a list of `analysis_id` values. Defaults to "Auto".
- `keep_replication` (Union[str, List[int]], optional): Specifies which replications to keep. Can be "None" or a list of `analysis_id` values. Defaults to "None".
- `filter` (dict, optional): A dictionary of filters to apply to the data. Defaults to None.

#### Returns

- `polars.DataFrame`: A DataFrame containing the filtered image quality reference data.

#### Examples

Retrieve specific image quality data with custom replication handling and filters:

```python
name = "example"
drop_replication = [1, 2]
keep_replication = "None"
filter = {"column1": ["value1", "value2"], "column2": ["value3"]}

result = get_image_quality_ref(name, drop_replication, keep_replication, filter)
# `result` is a DataFrame with the specified image quality data
```

!!! Info

     - The function initially retrieves image quality reference data using `_get_image_quality_reference_df`.
     - It logs information about the data retrieved, including the number of unique studies found and details of plate barcodes.
     - Based on `drop_replication` and `keep_replication` parameters, the function processes the DataFrame to retain or exclude specific replications.
     - If filters are provided, it applies them to the DataFrame, allowing for refined data retrieval based on specific conditions.
     - This flexibility in handling replications and applying filters makes the function highly adaptable for various scenarios to select the experiments.
     - The function's ability to sort and uniquely identify data based on experimental needs ensures that users receive the most relevant and accurate image quality data for their specific queries.


### `get_image_quality_data()`

Retrieves and processes image quality data based on provided filtered information. This function serves as the main workflow for extracting, processing, and merging image quality data, allowing for various handling options based on user requirements.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/dataset/image_quality.py#L193C1-L288C6)

```python
def get_image_quality_data(
    filtered_image_quality_info: pl.DataFrame,
    force_merging_columns: Union[bool, str] = False
) -> pl.DataFrame:
```

#### Parameters

- `filtered_image_quality_info` (pl.DataFrame): The filtered image quality information, typically obtained from the `get_image_quality_ref` function.
- `force_merging_columns` (Union[bool, str], optional): Specifies the method for merging columns. If set to `"keep"`, all columns are kept and missing values are filled with null. If `"drop"`, only matching columns are kept during horizontal merge. If `False`, the function returns `None`. Defaults to `False`.

#### Returns

- `pl.DataFrame`: The concatenated and processed image quality data.

#### Examples

Retrieve and process image quality data with specific merging preferences:

```python
filtered_image_quality_ref = get_image_quality_ref("experiment_name", drop_replication="Auto")
force_merging_columns = "keep"

result = get_image_quality_data(filtered_image_quality_ref, force_merging_columns)
# `result` is a DataFrame with processed image quality data
```

!!! Info

     - The function reads and processes files based on the information in `filtered_image_quality_info`, handling different file naming schemes and extensions.
     - It casts numerical columns to appropriate data types (e.g., Float64 to Float32) for consistency and efficiency.
     - The merging behavior is controlled by `force_merging_columns`, allowing for flexibility in how dataframes with different shape are combined.
     - It logs successful imports and warnings for missing files, providing transparency in the data processing workflow.
      - If `force_merging_columns` is set to "keep", the function merges the dataframes diagonally, ensuring that all columns are retained. In case of "drop", it keeps only the columns common across all dataframes.