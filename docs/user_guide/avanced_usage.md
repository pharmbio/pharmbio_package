# Avanced Usage

## Looking up the experiment in the database with name

Certainly, here's the concise version of the tutorial focusing on the usage of `get_projects_list()`:

### Using `get_projects_list()`

#### Basic Usage - Retrieving All Projects

To fetch the complete list of project names without any filters, simply call the function without passing any arguments. This is useful for getting an overview of all available projects in the database.

```python
project_list = get_projects_list()
print(project_list)
```

**Output Example:** `['Project A', 'Project B', 'Project C', ...]`

#### Filtered Search - Using the `lookup` Parameter

For more refined searches, use the `lookup` parameter. This is particularly helpful when dealing with large datasets where you need to find projects related to a specific topic or keyword.

```python
filtered_list = get_projects_list(lookup='aros')
print(filtered_list)
```

**Output Example:** `['AROS-CP', 'AROS-Reproducibility-MoA-Full', ...]`

!!!Note
   
    The search is case-insensitive and can match partial strings.

## Accessing Image Quality Data

### Using `get_image_quality_ref()` with Advanced Filtering

#### Introduction

The `get_image_quality_ref()` function, part of the `pharmbio.dataset.image_quality` module, is essential for retrieving quality control reference data from specific studies. This tutorial covers its advanced usage, particularly focusing on complex filtering techniques to refine the data retrieval process.

#### Step-by-Step Guide

1. **Basic Retrieval without Replication Dropping**
   Initially, you can retrieve all replications (including duplicates) by setting the `drop_replication` parameter to `"None"`. This will return every instance, replicated analysis IDs included.
   ```python
   qc_ref_df = get_image_quality_ref("sarscov2-repurposing", drop_replication="None")
   print(qc_ref_df)
   ```
2. **Filtering by Date**
   To focus on experiments conducted in a specific year, use the `filter` parameter. For instance, to view experiments from 2021:
   ```python
   qc_ref_df = get_image_quality_ref(
       "sarscov2-repurposing",
       drop_replication="None",
       filter={"analysis_date": ["2021"]},
   )
   print(qc_ref_df)
   ```
3. **Combining Multiple Filters**
   You can combine filters to further refine your search. For example, to view experiments from both 2021 and 2023:
   ```python
   qc_ref_df = get_image_quality_ref(
       "sarscov2-repurposing",
       drop_replication="None",
       filter={"analysis_date": ["2021", "2023"]},
   )
   print(qc_ref_df)
   ```
4. **Filtering by Specific Criteria**
   To get data from 2023 that used VeroE6 cells, add another key to the filter:
   ```python
   qc_ref_df = get_image_quality_ref(
       "sarscov2-repurposing",
       drop_replication="None",
       filter={"analysis_date": ["2023"], "plate_barcode": ["VeroE6"]},
   )
   print(qc_ref_df)
   ```
5. **Advanced Filtering with Partial Matches**
   For more specific searches, like filtering by a part of a string, you can include partial strings in the filter. For example, to find data with `plate_acq_id` starting with "37":
   ```python
   qc_ref_df = get_image_quality_ref(
       "sarscov2-repurposing",
       drop_replication="None",
       filter={
           "analysis_date": ["2023"],
           "plate_barcode": ["VeroE6"],
           "plate_acq_id": ["37"],
       },
   )
   print(qc_ref_df)
   ```

!!!Note  Key Points

      - **Flexible Filtering:** The `filter` argument accepts multiple keys and values. Values should be in list format and can be partial strings.
      - **String-Based Filtering:** Even numerical values should be passed as strings to enable partial matching.
      - **Combining Filters:** Filters act conjunctively, allowing for precise data retrieval based on multiple criteria.


## Flagging Outlier Images

### Advanced Functions in `pharmbio.data_processing.quality_control`

#### Introduction

The `pharmbio.data_processing.quality_control` module in Python provides an extensive set of functions for handling and analyzing image quality control data in biomedical research. This tutorial will cover the advanced functionalities of this module, specifically focusing on functions such as `get_qc_module`, `get_qc_data_dict`, `get_channels`, and `flag_outlier_images`.

#### 1. `get_qc_module`

**Purpose:** To extract and return a sorted list of image quality module names from the quality control data.

**Usage Example:**

```python
qc_data = get_image_quality_data(name='example')
qc_modules = get_qc_module(qc_data)
print(qc_modules)
```

#### 2. `get_qc_data_dict`

**Purpose:** To create a dictionary of image quality module data frames, filtered by specified modules to keep or drop.

**Usage Example:**

```python
qc_data = pd.DataFrame({
    'ImageQuality_FocusScore': [0.5, 0.6, 0.7],
    'ImageQuality_Intensity': [0.8, 0.9, 1.0],
    'OtherColumn': [1, 2, 3]
})
qc_data_dict = get_qc_data_dict(qc_data, module_to_keep={'FocusScore'})
print(qc_data_dict)
```

#### 3. `get_channels`

**Purpose:** To return a dictionary of channels and sub-channels for each QC module in the QC data.

**Usage Example:**

```python
qc_data = pd.DataFrame({
    'ImageQuality_FocusScore_CONC': [0.5, 0.6, 0.7],
    'ImageQuality_FocusScore_HOECHST': [0.8, 0.9, 1.0],
    'ImageQuality_Intensity_CONC': [1, 2, 3],
    'OtherColumn': ...
})
channels = get_channels(qc_data)
print(channels)
```

#### 4. `flag_outlier_images`

**Purpose:** To flag outlier images based on specified quality control data using either Standard Deviation (SD) or Interquartile Range (IQR) methods.

**Usage Example:**

### Deep Dive into `flag_outlier_images` Function

The `flag_outlier_images` function in the `pharmbio.data_processing.quality_control` module is designed to flag outlier images in a dataset based on certain statistical methods. It's a sophisticated function that allows for nuanced control over the outlier detection process. Let's break it down and examine its components and usage.

#### Function Parameters

1. **method (Literal["SD", "IQR"]):** The outlier detection method, either Standard Deviation ("SD") or Interquartile Range ("IQR").

2. **IQR_normalization (bool):** Determines whether to normalize the data when using the IQR method.

3. **normalization (Literal["zscore", "minmax"]):** The type of normalization to apply, either z-score or min-max normalization.

4. **sd_step_dict (Dict[str, Tuple[float, float]]):** A dictionary specifying the SD steps for each module.

5. **default_sd_step (Tuple[float, float]):** Default SD steps if `sd_step_dict` is not provided.

6. **quantile_limit (float):** The quantile limit for the IQR method.

7.  **multiplier (float):** The multiplier for the IQR method.

#### Examples of Usage

1. **Basic Usage with SD Method:**
   ```python
   qc_data = get_image_quality_data(name='example')
   flagged_data = flag_outlier_images(qc_data, method='SD')
   ```
2. **Using IQR Method with Specific Modules:**
   ```python
   flagged_data = flag_outlier_images(
    qc_data,
    module_to_keep={'FocusScore', 'Intensity'},
    method='IQR',
    multiplier=1.5)
   ```
3. **Applying Custom SD Range for Specific Modules:**
   ```python
   sd_step_dict = {'FocusScore': (-3, 3), 'Intensity': (-2, 2)}
   flagged_data = flag_outlier_images(qc_data, method='SD', sd_step_dict=sd_step_dict)
   ```
4. **Combining Module Filtering and Normalization:**
   ```python
   flagged_data = flag_outlier_images(
    qc_data, module_to_keep={'FocusScore'},
    module_to_drop={'Intensity'},
    normalization='minmax',
    method='SD')
   ```

!!!Note Key Points

      - **Flexibility:** These functions provide flexibility in processing and analyzing QC data by allowing the selection of specific modules and methods for outlier detection.
      - **Customization:** You can customize the filtering process with `module_to_keep` and `module_to_drop` to target specific QC modules.
      - **Outlier Detection:** `flag_outlier_images` offers robust outlier detection with options for normalization and threshold setting.


## Retrieving Cell Morphology Data

### Exploring the `pharmbio.dataset.cell_morphology` Module

The `pharmbio.dataset.cell_morphology` module provides a suite of functions specifically designed to handle and query cell morphology data. Each function serves a unique purpose, catering to various aspects of data handling, from retrieval and outlier detection to data aggregation. Let's delve into the details of these functions.

#### 1. `get_cell_morphology_ref()`

- **Purpose:** Retrieves cell morphology references from a database, allowing users to specify a reference name and apply filtering.
- **Parameters:**
  - `name`: A mandatory parameter specifying the reference name.
  - `filter`: An optional dictionary for filtering the query.
- **Usage Example:**
  ```python
  name = "example_reference"
  filter = {"column1": ["value_1", "value2"], "column2": ["value3"]}
  filtered_df = get_cell_morphology_ref(name, filter)
  display(filtered_df)
  ```
- **Key Point:** This function is crucial for extracting specific cell morphology data and supports complex query constructions using filters.

#### 2. `get_outlier_df()`

- **Purpose:** Retrieves a DataFrame containing detailed information about outliers from flagged QC data.
- **Parameters:**
  - `flagged_qc_df`: A DataFrame containing flagged QC data.
  - `with_compound_info`: Optionally includes compound-related information.
- **Usage Example:**
  ```python
  flagged_qc_df = # Pre-existing DataFrame with flagged QC data
  outlier_df = get_outlier_df(flagged_qc_df)
  print(outlier_df)
  ```
- **Key Point:** This function is essential for detailed outlier analysis in cell morphology studies, offering an optional inclusion of compound information.

#### 3. `get_comp_outlier_info()`

- **Purpose:** Computes and provides detailed information about outliers in a dataset.
- **Parameters:**
  - `flagged_df`: A DataFrame with flagged data, including batch identification and outlier flags.
- **Usage Example:**
  ```python
  flagged_df = # Pre-existing DataFrame with flagged data
  outlier_info_df = get_comp_outlier_info(flagged_df)
  ```
- **Key Point:** It's vital for understanding the impact of outliers on data, particularly useful in large-scale studies involving numerous compounds.

#### 4. `get_cell_morphology_data()`

- **Purpose:** Aggregates cell morphology data from various sources, incorporating user-defined parameters for detailed analysis.
- **Parameters:**
    - `cell_morphology_ref_df`: The main DataFrame containing cell morphology data.
    - `flagged_qc_df`: (Optional) DataFrame with flagged QC data to identify outliers.
    - `site_threshold`: Numeric threshold for flagged sites in a well.
    - `compound_threshold`: Numeric threshold for percentage of data loss.
    - `aggregation_level`: Level of data aggregation (e.g., "cell", "well").
    - `aggregation_method`: Methods for aggregation (e.g., "mean", "median").
    - `path_to_save`: Path to save the aggregated data.
    - `use_gpu`: Option to use GPU for faster processing.
    - `save_plate_separately`: Whether to save data for each plate separately.
- **Data Integration:** It combines reference cell morphology data (`cell_morphology_ref_df`) with quality control data (`flagged_qc_df`), if provided.
- **Threshold-Based Outlier Handling:** The function allows for the exclusion of data based on the number of flagged sites in a well (`site_threshold`) and the percentage of data loss at which a compound is flagged (`compound_threshold`).
- **Flexible Aggregation:** Aggregates data at specified levels (`aggregation_level`) like cell, site, well, plate, or compound, using various methods (`aggregation_method`).

- **Usage Example:**
    1. **Basic Aggregation at the Cell Level:**
       Aggregates data at the cell level without considering outliers.
       ```python
       cell_morphology_ref_df = get_cell_morphology_ref("example_reference")
       aggregated_df = get_cell_morphology_data(cell_morphology_ref_df, aggregation_level='cell')
       display(aggregated_df)
       ```
    2. **Aggregation with Outlier Data at the Well Level:**
       Uses flagged QC data to remove outlier wells before aggregation.
       ```python
       flagged_qc_df = # Assume pre-existing DataFrame with flagged QC data
       aggregated_df = get_cell_morphology_data(
           cell_morphology_ref_df,
           flagged_qc_df,
           site_threshold=5,  # Wells with more than 5 flagged sites are removed
           aggregation_level='well'
       )
       display(aggregated_df)
       ```
    3. **Aggregation with Compound Deletion Threshold:**
       Removes compounds with a high percentage of data loss.
       ```python
       aggregated_df = get_cell_morphology_data(
           cell_morphology_ref_df,
           flagged_qc_df,
           compound_threshold=0.6,  # Compounds with more than 60% data loss are removed
           aggregation_level='compound'
       )
       display(aggregated_df)
       ```
    4. **Custom Aggregation Method:**
       Aggregates data using a custom method, such as median, for each level.
       ```python
       aggregation_method = {"cell": "median", "well": "median", "plate": "median"}
       aggregated_df = get_cell_morphology_data(
           cell_morphology_ref_df,
           aggregation_level='plate',
           aggregation_method=aggregation_method
       )
       display(aggregated_df)
       ```
    5. **Utilizing GPU Acceleration:**
       Aggregates data using GPU acceleration for large datasets.
       ```python
       aggregated_df = get_cell_morphology_data(
           cell_morphology_ref_df,
           use_gpu=True,
           aggregation_level='plate'
       )
       display(aggregated_df)
       ```

#### Conclusion

`get_cell_morphology_data` offers versatile solutions for cell morphology data analysis. Its ability to integrate different data sources, handle outliers based on user-defined thresholds, and perform custom aggregation makes it a valuable tool for researchers. By selecting appropriate parameters, you can tailor the function to meet the specific needs of your study, ensuring efficient and meaningful data analysis.

!!!Note
        - This function is a comprehensive tool for cell morphology data management, offering flexibility in handling outlier data and custom aggregation methods.


### Explanation of the `Experiment` Class

The `Experiment` class is a tool designed for automating the process of handling and analyzing cell morphology and image quality data in the `pharmbio` package. It integrates various functions from the `pharmbio.dataset.cell_morphology` and `pharmbio.dataset.image_quality` modules, streamlining data processing tasks. The class is initialized with parameters defined in a JSON file, providing an easy and customizable approach to experiment management.

#### Class Overview

- **Initialization:** The class is instantiated with a JSON file that includes experiment settings, such as `experiment_name`, `filter`, `module_to_keep`, etc.
- **Attributes:** The class maintains several attributes related to image quality, cell morphology, outlier detection, and aggregation.
- **Methods:** It includes methods for retrieving and processing data, aggregating results, and generating visualizations.

#### Key Methods

1. **Data Retrieval Methods:**
      - `get_image_quality_reference_data()`: Retrieves image quality reference data.
      - `get_cell_morphology_reference_data()`: Retrieves cell morphology reference data.

2. **Data Processing Methods:**
      - `get_image_quality_data()`: Processes image quality data.
      - `get_cell_morphology_data()`: Processes and aggregates cell morphology data.

3. **Outlier Analysis Methods:**
      - `flag_outlier_images()`: Flags outlier images in the dataset.
      - `get_image_guality_modules()`, `get_image_guality_data_dict()`: Retrieve and organize image quality data.

4. **Visualization Methods:**
      - `plate_heatmap()`, `well_outlier_heatmap()`, `quality_module_lineplot()`: Generate various plots for data visualization.

5. **Utility Methods:**
      - `print_setting()`: Prints the current settings of the experiment.

#### JSON File Structure

The JSON file serves as the configuration for the experiment. It specifies parameters like:

- `experiment_name`: The name of the experiment.
- `filter`: Conditions for data filtering.
- `force_merging_columns`: Handling of merging columns.
- `module_to_keep`: Modules to include in analysis.
- `method`: Method for outlier detection.
- `site_threshold`, `compound_threshold`: Thresholds for data exclusion.
- `aggregation_level`: Level of data aggregation.

#### Usage Example

With the provided JSON file which is just values for the arguments that exist in different function used above we can initiate a class instant that include all data and plot for specific experiment:

```json
{
    "experiment_name": "AROS-Reproducibility-MoA-Full",
    "filter": {
        "analysis_id": [
            "3248",
            "3249"
        ]
    },
    "force_merging_columns": "keep",
    "module_to_keep": [
        "FocusScore",
        "MaxIntensity",
        "MeanIntensity",
        "PowerLogLogSlope",
        "StdIntensity"
    ],
    "method": "SD",
    "site_threshold": 4,
    "compound_threshold": 0.7,
    "aggregation_level": "cell"
}
```

This JSON file serves as a configuration for initializing the `Experiment` class, detailing the parameters for the experiment's data processing and analysis. An `Experiment` object can be created and used to automate data retrieval, processing, and analysis tasks:

```python
experiment = Experiment(json_file="path_to_json_file.json")
```

Using the methods and attributes of the `Experiment` class, one can perform a comprehensive analysis of the experiment data, from quality control to cell morphology analysis, and visualize the results efficiently.

!!!Info "JSON File Composition"
    1. **Specify Mandatory Fields:**
          - Always include `experiment_name` as it's essential for identifying the dataset.
    2. **Optional Fields:**
          - Fields like `filter`, `module_to_keep`, and others are optional. If not provided, the class will use default values or behaviors.
    3. **Using Filters and Selections:**
          - Define filters (e.g., `filter`) and module selections (`module_to_keep`) as arrays, even if only one value is needed.
    4. **Setting Thresholds and Parameters:**
          - Include parameters like `site_threshold` and `compound_threshold` to customize data processing. Absence of these will result in the use of default thresholds.

!!!Info  "Class Behavior and Default Settings"
    1. **Default Values:**
          - When a variable is not specified in the JSON, the class uses predefined default values. For example, the default for `site_threshold` might be set to 6 if not specified.
    2. **Flexible Data Handling:**
          - The class can handle various scenarios, such as missing data or unspecified parameters, by resorting to default processing methods or skipping certain steps.
    3. **Error Handling:**
          - Ensure proper formatting and valid values in the JSON file to prevent runtime errors. For instance, numeric fields should not contain non-numeric characters.
    4. **Modular Approach:**
          - Each method within the class is responsible for a specific aspect of the experiment's data processing. This modular design facilitates troubleshooting and customization.

#### Conclusion

The `Experiment` class, when used with a well-structured JSON configuration file, provides a powerful and flexible way to automate and manage data processing tasks in cell morphology and image quality analysis. By adhering to these guidelines, researchers can efficiently configure and execute their experiments with greater control and customization.