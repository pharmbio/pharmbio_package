## `pharmbio.dataset.experiment`

This module contains functions related to handling and querying experiment-related data in the `pharmbio` package.

### `get_projects_list()` 

Retrieves a list of project names from the database, with an optional filter to return only those projects that contain a specified substring in their names.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/experiment.py#L22)

```python
def get_projects_list(lookup: str = None) -> list:
```

#### Parameters

- `lookup` (str, optional): A string to filter the project list. If provided, the function returns only those projects that contain the `lookup` string in their names. The search is case-insensitive and the `lookup` string can match any part of a project name. Defaults to `None`, which returns all project names.

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


### `Experiment`

This class encapsulates an entire experiment, providing functionalities to load, process, and analyze various aspects of experimental data.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/experiment.py#L59C1-L207C51)

```python
class Experiment:
    def __init__(self, json_file: str):
```

#### Parameters

- `json_file` (str): The path to a JSON file containing the experiment's data. This file should contain relevant information needed to initialize and populate the experiment's attributes.

#### Attributes

- `image_quality_data`: Stores the image quality data related to the experiment.
- `flagged_image_quality_data`: Contains image quality data that has been flagged for quality issues.
- `cell_morphology_data`: Holds cell morphology data from the experiment.
- `compound_batch_ids`: A list of IDs associated with different compound batches used in the experiment.
- `compound_outlier_info`: Information about outliers identified in the experiment's flagged image quality data.
- `outlier_dataframe`: A DataFrame that includes detailed outlier information for the experiment's flagged image quality data.

#### Methods

- `get_image_quality_reference_data()`: Returns reference data for image quality analysis.
- `get_image_quality_data()`: Retrieves and processes image quality data based on the provided reference data.
- `get_cell_morphology_reference_data()`: Returns reference data for cell morphology analysis.
- `get_cell_morphology_data()`: Retrieves and processes cell morphology data based on the provided reference data.
- `get_image_quality_modules()`: Returns the image quality modules used in the experiment.
- `get_image_quality_data_dict()`: Provides a dictionary representation of the image quality data.
- `flag_outlier_images()`: Identifies and flags outlier images based on specified criteria.
- `plate_heatmap(...)`: Generates heatmaps for the given plates in the experiment.
- `well_outlier_heatmap()`: Creates a heatmap for well outliers in the experiment.
- `quality_module_lineplot(...)`: Plots a line graph for the selected quality modules.
- `print_setting()`: Prints the current settings and configuration of the experiment in a readable format.

#### Examples

To initialize an `Experiment` instance with a specified JSON file:
```python
experiment = Experiment('path/to/experiment_data.json')
```

To retrieve and print the image quality data:
```python
image_quality_data = experiment.get_image_quality_data()
```

To generate a heatmap for a specific plate:
```python
experiment.plate_heatmap()
```

!!! Info

    - The `Experiment` class is a comprehensive tool for handling complex experimental data, particularly in the fields of cell morphology and compound analysis.
    - It is important to provide a correctly formatted JSON file to ensure proper initialization of the experiment.
    - Some methods of the `Experiment` class might require additional dependencies to be installed or specific configurations to be set in your working environment.

## `pharmbio.dataset.cell_morphology`

This module contains functions related to handling and querying cell morphology data in the `pharmbio` package.

### `get_cell_morphology_ref()`

Retrieves cell morphology references from a specified database, allowing users to specify a reference name and apply optional filtering conditions to refine the search results. This function is particularly useful for extracting specific cell morphology data based on user-defined criteria.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L22)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L74)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L114)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L143)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L166)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L196)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L222)

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

### `_get_morphology_feature_cols()`

This function is designed to extract and return the names of columns in a DataFrame that correspond to morphology features.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L245)

```python
def _get_morphology_feature_cols(df: pl.DataFrame) -> List[str]:
```

#### Parameters

- `df` (`polars.DataFrame`): The original DataFrame from which morphology feature columns need to be identified.

#### Returns

- `List[str]`: A list of column names that represent morphology features in the provided DataFrame. The list excludes specific columns like the count of nuclei and cytoplasm in cells.

#### Examples

To obtain a list of morphology feature column names from a DataFrame:
```python
df = # Assume this is a pre-existing DataFrame with cell morphology data
morphology_feature_cols = _get_morphology_feature_cols(df)
print("Morphology Feature Columns:", morphology_feature_cols)
```

!!! Info

    - The `_get_morphology_feature_cols` function is essential for preprocessing steps in cell morphology analysis, where specific feature columns need to be isolated for further analysis.
    - It automatically filters out non-numeric columns and specific count columns to provide a refined list of relevant features.
    - This function is especially useful in scenarios where datasets contain a mix of morphology-related and non-related data, aiding in efficient data processing and analysis.

### `_reorder_dataframe_columns()`

Reorders the columns in a dataframe based on data types and specific columns. This function is designed to organize dataframe columns in a systematic manner, enhancing readability and analysis efficiency. It is intended for internal use within the `cell_morphology` module.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L260)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L283)

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

### `get_outlier_df()`

This function retrieves a DataFrame containing detailed outlier information from flagged quality control data, particularly useful in cell morphology analysis.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L319C1-L364C6)

```python
def get_outlier_df(flagged_qc_df: pl.DataFrame, with_compound_info: bool = False) -> pl.DataFrame:
```

#### Parameters

- `flagged_qc_df` (`polars.DataFrame`): A DataFrame containing flagged quality control data. This data is used to identify and analyze outliers in the dataset.
- `with_compound_info` (`bool`, optional): A flag to include compound-related information in the returned DataFrame. If set to `True`, additional compound-related columns such as batch ID, SMILES notation, InChI, and InChIKey are included. Defaults to `False`.

#### Returns

- `polars.DataFrame`: A DataFrame containing detailed outlier information. This DataFrame includes columns for acquisition ID, barcode, well, and the number of outliers. It also features a range of integers from 1 to 10 and, optionally, compound-related information if `with_compound_info` is set to `True`.

#### Examples

To obtain a DataFrame with outlier information from a flagged quality control DataFrame:
```python
flagged_qc_df = # Assume this is a pre-existing DataFrame with flagged QC data
outlier_df = get_outlier_df(flagged_qc_df)
print(outlier_df)
```

To include compound information in the outlier DataFrame:
```python
outlier_df_with_compound = get_outlier_df(flagged_qc_df, with_compound_info=True)
print(outlier_df_with_compound)
```

!!! Info

    - The `get_outlier_df` function is crucial for detailed analysis of outliers in cell morphology datasets, allowing researchers to pinpoint specific areas of concern.
    - The inclusion of compound information can be particularly useful for studies involving chemical screenings or compound-effect analysis.
    - The function relies on the `polars` library for DataFrame operations, ensuring efficient and fast data manipulation.


### `_outlier_series_to_delete()`

This function is designed to identify and flag outliers in a Polars DataFrame related to cell morphology data. It determines which compounds and image IDs of sites should be considered for deletion based on specified thresholds.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L367C1-L439C55)

```python
def _outlier_series_to_delete(
    flagged_qc_df: pl.DataFrame, 
    site_threshold: int = 6, 
    compound_threshold: float = 0.7
) -> (pl.Series, pl.Series, pl.DataFrame):
```

#### Parameters

- `flagged_qc_df` (`polars.DataFrame`): A DataFrame containing quality control data with an 'outlier_flag' column. This data is used for identifying outliers.
- `site_threshold` (`int`, optional): The threshold for the number of sites in a well above which all sites are considered outliers. The valid range is 1-9. Defaults to 6.
- `compound_threshold` (`float`, optional): The threshold for the percentage of data loss at which a compound is considered for deletion. The valid range is 0-1. Defaults to 0.7.

#### Returns

- A tuple containing two `polars.Series` and a `polars.DataFrame`:
    - The first series contains the identifiers of the compounds to be deleted.
    - The second series includes image IDs of sites to be deleted.
    - The returned DataFrame is used internally for the calculation of these series.

#### Examples

To identify compounds and image IDs of sites to delete based on outlier analysis:
```python
flagged_qc_df = # Assume this is a pre-existing DataFrame with flagged QC data
compounds_to_delete, images_to_delete = _outlier_series_to_delete(flagged_qc_df)
print("Compounds to delete:", compounds_to_delete)
print("Image IDs to delete:", images_to_delete)
```

!!! Info

    - The `_outlier_series_to_delete` function plays a crucial role in maintaining the integrity of cell morphology datasets by removing unreliable data points.
    - It's important to set appropriate thresholds for both site and compound deletion to ensure accurate data analysis.
    - This function is typically used in more advanced stages of data processing where precise outlier removal can significantly impact the quality of the analysis.


### `get_comp_outlier_info()`

This function computes outlier information for a given DataFrame that contains flagged data. It is particularly useful in the analysis of cell morphology data where identifying and quantifying outliers is crucial.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3a4500aef3a2c0059379849bf43f6e6af396cf72/pharmbio/dataset/cell_morphology.py#L442)

```python
def get_comp_outlier_info(flagged_df: pl.DataFrame) -> pl.DataFrame:
```

#### Parameters

- `flagged_df` (`polars.DataFrame`): A DataFrame containing flagged data. The data should include columns for batch identification and outlier flags.

#### Returns

- A `polars.DataFrame`: This DataFrame includes the following columns:
    - `batch_id`: Identifier for each batch.
    - `outlier_img_num`: The number of outlier images per compound.
    - `total_img_num`: The total number of images per compound.
    - `lost_data_percentage`: The percentage of data considered as lost due to outliers.

The returned DataFrame is sorted in descending order based on the number of outlier images.

#### Examples

To calculate the outlier information for a given DataFrame:

```python
flagged_df = # Assume this is a pre-existing DataFrame with flagged data
outlier_info_df = get_comp_outlier_info(flagged_df)
```

!!! Info

    - The `get_comp_outlier_info` function is essential for understanding the distribution and impact of outliers in your data.
    - It helps in the decision-making process regarding data cleaning and preprocessing, especially in large datasets with numerous compounds.
    - Sorting the DataFrame based on the number of outlier images provides a clear view of which compounds are most affected by outliers.

### `get_cell_morphology_data()`

Retrieves, processes, and aggregates cell morphology data from specified reference and flagged QC dataframes, utilizing user-defined parameters for detailed and nuanced analysis. This enhanced function now offers more flexibility in handling outlier data and custom aggregation methods, making it a central feature in the `pharmbio` package for cell morphology data management.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/cell_morphology.py#L476C1-L703C6)

```python
def get_cell_morphology_data(
    cell_morphology_ref_df: Union[pl.DataFrame, pd.DataFrame],
    flagged_qc_df: Union[pl.DataFrame, pd.DataFrame] = None,
    site_threshold: int = 6,
    compound_threshold: float = 0.7,
    aggregation_level: str = "cell",
    aggregation_method: Optional[Dict[str, str]] = None,
    path_to_save: str = "data",
    use_gpu: bool = False,
    save_plate_separately: bool = False
) -> pl.DataFrame:
```

#### Parameters

- `cell_morphology_ref_df` (Union[pl.DataFrame, pd.DataFrame]): The reference DataFrame containing cell morphology data.
- `flagged_qc_df` (Union[pl.DataFrame, pd.DataFrame], optional): Quality control DataFrame with flagged outlier images. Defaults to `None`.
- `site_threshold` (int, optional): Threshold for the number of flagged sites in a well, above which the whole well is considered for removal. Range: 1-9. Defaults to 6.
- `compound_threshold` (float, optional): Threshold for the percentage of data loss at which a compound is considered for deletion. Range: 0-1. Defaults to 0.7.
- `aggregation_level` (str, optional): Level at which data aggregation is performed. Options: "cell", "site", "well", "plate", "compound". Defaults to "cell".
- `aggregation_method` (Dict[str, str], optional): Methods of aggregation for each level, such as "mean", "median", etc. Defaults to `None`.
- `path_to_save` (str, optional): Path for saving the aggregated data. Defaults to "data".
- `use_gpu` (bool, optional): Flag for using GPU acceleration. Defaults to `False`.
- `save_plate_separately` (bool, optional): Indicates whether to save aggregated data for each plate separately. Defaults to `False`.

#### Returns

- `pl.DataFrame`: The aggregated cell morphology data as a DataFrame.

#### Raises

- `EnvironmentError`: Raised when GPU acceleration is requested but not available.
- `ValueError`: Raised for invalid `site_threshold` or `compound_threshold` values.

#### Examples

To aggregate cell morphology data at the plate level, considering flagged QC data:

```python
cell_morphology_ref_df = get_cell_morphology_ref("example_reference")
flagged_qc_df = # Assume pre-existing DataFrame with flagged QC data
aggregated_df = get_cell_morphology_data(
    cell_morphology_ref_df,
    flagged_qc_df,
    site_threshold=6,
    compound_threshold=0.7,
    aggregation_level='plate'
)
display(aggregated_df)
```

!!! Info

    - The function can optionally incorporates outlier handling based on flagged QC data, enhancing its robustness and reliability in processing complex cell morphology datasets.
    - It offers flexible aggregation options at multiple levels, allowing for tailored analysis suited to specific experimental needs.
    - GPU acceleration, if available, can significantly speed up data processing, especially for large datasets.
    - The function takes a holistic approach to data aggregation, covering various steps such as data cleaning, joining, column reordering, and merging with additional plate information.
    - The final output is a comprehensive and highly customizable DataFrame, enabling in-depth analysis of cell morphology data.

## `pharmbio.dataset.image_quality`

This module in the `pharmbio` package is dedicated to handling and querying image quality data.

### `_get_image_quality_reference_df()`

Retrieves an image quality reference dataframe along with an associated data dictionary from the database for a given experiment. This function is essential for obtaining image quality metadata and plate barcodes pertinent to a specific experiment, providing a foundation for image quality analysis.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/image_quality.py#L23)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/image_quality.py#L55)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/image_quality.py#L112)

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

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/aff7659f9ff41aec655f0f57e70217a1ac9e18d7/pharmbio/dataset/image_quality.py#L193)

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