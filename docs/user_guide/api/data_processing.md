## `pharmbio.data_processing.feature_aggregation`

This module contains functions designed to perform data aggregation tasks efficiently, utilizing either CPU or GPU resources. Here's a breakdown of its key purposes:

### `aggregate_data_cpu()`

Aggregates morphology data using specified columns and an aggregation function on CPU.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/data_processing/feature_aggregation.py#L11)

```python
def aggregate_data_cpu(
    df: Union[pl.DataFrame, pd.DataFrame],
    columns_to_aggregate: List[str],
    groupby_columns: List[str],
    aggregation_function: str = "mean",
) -> pl.DataFrame:
```

#### Parameters

- `df` (Union[pl.DataFrame, pd.DataFrame]): The input DataFrame to be aggregated. Can be either a Polars or Pandas DataFrame.
- `columns_to_aggregate` (List[str]): List of column names to be aggregated.
- `groupby_columns` (List[str]): List of column names to group by.
- `aggregation_function` (str, optional): The aggregation function to be applied. Defaults to "mean". Other possible values include "median", "sum", "min", "max".

#### Returns

- `pl.DataFrame`: The aggregated Polars DataFrame.

#### Examples

```python
df = pl.DataFrame({
    'A': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    'B': [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2],
    'C': [9, 10, 11, 12, 9, 10, 11, 12, 12, 11, 12],
    'D': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]})

aggregate_data_cpu(df, columns_to_aggregate=['B', 'C'], groupby_columns=['A'], aggregation_function='mean')
```

### `aggregate_data_gpu()`

Aggregates data using specified columns and an aggregation function with GPU acceleration.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/data_processing/feature_aggregation.py#L67)

```python
def aggregate_data_gpu(
    df: Union[pl.DataFrame, pd.DataFrame],
    columns_to_aggregate: List[str],
    groupby_columns: List[str],
    aggregation_function: str = "mean",
) -> pl.DataFrame:
```

#### Parameters

- Same as `aggregate_data_cpu`.

#### Returns

- `pl.DataFrame`: The aggregated DataFrame.

#### Raises

- `ImportError`: Raised when the CuPy package is not available.
- `RuntimeError`: Raised when an unexpected error occurs during the aggregation process.

#### Examples

```python
df = pd.DataFrame({


    'A': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
    'B': [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2],
    'C': [9, 10, 11, 12, 9, 10, 11, 12, 12, 11, 12],
    'D': [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]})

aggregate_data_gpu(df, columns_to_aggregate=['B', 'C'], groupby_columns=['A'], aggregation_function='mean')
```

!!! Info

    - The GPU-accelerated version (`aggregate_data_gpu`) requires the CuPy package for execution. Ensure that it is installed and configured correctly in your environment for optimal performance.
    - GPU acceleration is beneficial for large datasets, where it can significantly speed up the aggregation process compared to CPU-based aggregation.


## `pharmbio.data_processing.quality_control`

This module includes functions `get_qc_module`, `get_qc_data_dict`, `get_channels`, and `flag_outlier_images` to performe all neccessary part of the quality control on the data:


### `get_qc_module()`

Returns a sorted list of image quality module names extracted from the given QC data.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/data_processing/quality_control.py#L12)


```python
def get_qc_module(qc_data: Union[pl.DataFrame, pd.DataFrame]) -> List[str]:
```

#### Parameters

- `qc_data` (Union[pl.DataFrame, pd.DataFrame]): QC data containing columns related to image quality.

#### Returns

- `List[str]`: A sorted list of QC module names.

#### Example

```python
qc_data = get_image_quality_ref('AROS-Reproducibility-MoA-Full')
qc_modules = get_qc_module(qc_data)
print(qc_modules)

# output: ['Correlation', 'FocusScore', 'LocalFocusScore', ... ]
```

### `get_qc_data_dict()`

Returns a dictionary of image quality module data frames filtered by the specified modules.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/data_processing/quality_control.py#L38)

```python
def get_qc_data_dict(
    qc_data: Union[pl.DataFrame, pd.DataFrame],
    module_to_keep: Set[str] = None,
    module_to_drop: Set[str] = None
) -> Dict[str, pl.DataFrame]:
```

#### Parameters

- `qc_data` (Union[pl.DataFrame, pd.DataFrame]): QC data containing columns related to image quality.
- `module_to_keep` (Set[str], optional): Set of QC modules to keep.
- `module_to_drop` (Set[str], optional): Set of QC modules to drop.

#### Returns

- `Dict[str, pl.DataFrame]`: Dictionary of QC data frames filtered by specified modules.

#### Example

```python
qc_data_dict = get_qc_data_dict(qc_data, module_to_keep={'FocusScore'})
print(qc_data_dict)
```

### `get_channels()`

Returns a dictionary of channels

 and sub-channels for each QC module in the given QC data.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/data_processing/quality_control.py#L101)

```python
def get_channels(
    qc_data: Union[pl.DataFrame, pd.DataFrame],
    qc_module_list: List[str] = None,
    out_put: str = "dict"
) -> Dict[str, Dict[str, List[str]]]:
```

#### Parameters

- `qc_data` (Union[pl.DataFrame, pd.DataFrame]): The QC data containing columns related to image quality.
- `qc_module_list` (List[str], optional): The list of QC modules to consider.
- `out_put` (str, optional): The output format ("dict" or "print").

#### Returns

- `Dict[str, Dict[str, List[str]]]`: A dictionary of channels and sub-channels for each QC module.

#### Example

```python
qc_data = pd.DataFrame({
    'ImageQuality_FocusScore_CONC': [0.5, 0.6, 0.7],
    'ImageQuality_FocusScore_HOECHST': [0.8, 0.9, 1.0],
    'ImageQuality_Intensity_CONC': [1, 2, 3],
    'OtherColumn': ...
})
channels = get_channels(qc_data)
print(channels)

# Output:{'FocusScore': {'channels': ['CONC', 'HOECHST'], 'sub_channels': []},
#         'Intensity': {'channels': ['CONC'], 'sub_channels': []}
```

### `flag_outlier_images()`

Flags outlier images based on specified quality control (QC) data.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/data_processing/quality_control.py#L167)

```python
def flag_outlier_images(
    qc_data: Union[pl.DataFrame, pd.DataFrame],
    module_to_keep: Set[str] = None,
    module_to_drop: Set[str] = None,
    method: Literal["SD", "IQR"] = "SD",
    IQR_normalization: bool = True,
    normalization: Literal["zscore", "minmax"] = "zscore",
    sd_step_dict: Dict[str, Tuple[float, float]] = None,
    default_sd_step: Tuple[float, float] = (-4.5, 4.5),
    quantile_limit: float = 0.25,
    multiplier: float = 1.5
) -> pl.DataFrame:
```

#### Parameters

- `qc_data` (Union[pl.DataFrame, pd.DataFrame]): QC data containing columns related to image quality.
- `module_to_keep` (Set[str], optional): Set of QC modules to keep.
- `module_to_drop` (Set[str], optional): Set of QC modules to drop.
- `method` (Literal["SD", "IQR"], optional): Method used for outlier detection ("SD" for standard deviation or "IQR" for interquartile range). Defaults to "SD".
- `IQR_normalization` (bool, optional): Whether to perform IQR normalization. Applicable when method is "IQR". Defaults to True.
- `normalization` (Literal["zscore", "minmax"], optional): Normalization method ("zscore" or "minmax"). Defaults to "zscore".
- `sd_step_dict` (Dict[str, Tuple[float, float]], optional): Dictionary specifying SD steps for each module.
- `default_sd_step` (Tuple[float, float], optional): Default SD steps for outlier detection set to (-4.5, 4.5).
- `quantile_limit` (float, optional): Quantile limit for IQR method. Defaults to 0.25.
- `multiplier` (float, optional): Multiplier for IQR method. Defaults to 1.5.

#### Returns

- `pl.DataFrame`: QC data with flagged outlier images based on specified criteria.

#### Raises

- `ValueError`: If the quantile limit or multiplier is not within the specified range.

#### Example

```python
qc_data = get_image_quality_data(name='AROS-Reproducibility-MoA-Full')
flagged_qc_data = flag_outlier_images(qc_data, module_to_keep={'FocusScore'})
print(flagged_qc_data)
```
