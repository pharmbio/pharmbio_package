### `plate_heatmap()`

Generates a heatmap visualization for plate data, providing insights into spatial distribution patterns across wells in a microplate format.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/visualization/plots.py#L19)

```python
def plate_heatmap(
    df: Union[pl.DataFrame, pd.DataFrame],
    plate_names: List[str] = None,
    subplot_num_columns: int = 2,
    plot_size: int = 400,
    measurement: str = "Count_nuclei",
    plate_well_columns: Dict[str, str] = None
):
```

#### Parameters

- `df` (Union[pl.DataFrame, pd.DataFrame]): The input data frame, either a polars or pandas DataFrame, containing the plate and well metadata along with measurement data.
- `plate_names` (List[str], optional): A list of plate names to be visualized. If not provided, the function attempts to derive it from the data frame.
- `subplot_num_columns` (int, optional): Number of columns for subplot layout. Default is 2.
- `plot_size` (int, optional): Size of each subplot. Default is 400.
- `measurement` (str, optional): The name of the measurement column in the data frame. Default is "Count_nuclei".
- `plate_well_columns` (Dict[str, str], optional): A dictionary mapping the column names in `df` to the standard plate and well identifiers. Defaults to `{"plates": "Metadata_Barcode", "wells": "Metadata_Well"}`.

#### Returns

- The function does not return a value but displays the generated heatmap visualization directly.

#### Example

```python
import pandas as pd
from pharmbio_package.pharmbio.visualization.plots import plate_heatmap

# Sample DataFrame
data = {
    "Metadata_Barcode": ["Plate1", "Plate1", "Plate2", "Plate2"],
    "Metadata_Well": ["A01", "A02", "B01", "B02"],
    "Count_nuclei": [10, 15, 5, 20]
}
df = pd.DataFrame(data)

# Generating the heatmap
plate_heatmap(df)
```


### `_lineplot()` 
Internal function used to generate line plots for different data frames.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/visualization/plots.py#L147)


```python
def _lineplot(
    data_frames: pl.DataFrame,
    colors: List[str],
    title: str,
    plate_names: List[str],
    plot_size: int = 1400,
    normalization: bool = True,
    normalization_method: Literal["zscore", "minmax"] = "zscore",
    y_axis_range: Tuple = (-5, 5)
):
```

#### Parameters

This function is intended for internal use and may have dependencies on other parts of the `pharmbio_package`.


### `quality_module_lineplot()`

Generates line plots for quality control modules, allowing for visualization of quality metrics across different plates.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/visualization/plots.py#L263)


```python
def quality_module_lineplot(
    df: Union[pl.DataFrame, pd.DataFrame],
    qc_module_to_plot: Set[str] = None,
    title: str = "Unnamed",
    plot_size: int = 1400,
    normalization: bool = True,
    normalization_method: Literal["zscore", "minmax"] = "zscore",
    y_axis_range: Tuple = (-5, 5),
    colors: List[str] = COLORS
):
```

#### Parameters

- `df` (Union[pl.DataFrame, pd.DataFrame]): The input data frame, either a polars or pandas DataFrame, containing quality control data.
- `qc_module_to_plot` (Set[str], optional): A set of quality control modules to plot. If not provided, default QC modules are used.
- `title` (str, optional): Title of the plot. Default is "Unnamed".
- `plot_size` (int, optional): The width of the plot in pixels. Default is 1400.
- `normalization` (bool, optional): Whether to normalize data. Default is True.
- `normalization_method` (Literal["zscore", "minmax"], optional): Method used for normalization, either "zscore" or "minmax". Default is "zscore".
- `y_axis_range` (Tuple, optional): The range of the y-axis. Default is (-5, 5).
- `colors` (List[str], optional): List of colors for the line plots. Default is defined by `COLORS`.

#### Returns

- The function does not return a value but displays the generated line plots directly.

#### Example

```python
import pandas as pd
from pharmbio_package.pharmbio.visualization.plots import quality_module_lineplot

# Sample DataFrame
qc_data = {
    "Metadata_Barcode": ["Plate1", "Plate1", "Plate2", "Plate2"],
    "QC_Measure1": [0.5, 0.7, 0.

6, 0.4],
    "QC_Measure2": [0.3, 0.2, 0.1, 0.4]
}
df = pd.DataFrame(qc_data)

# Generating quality module line plots
quality_module_lineplot(df)
```

### `pad_with_zeros()`

A utility function to pad a given vector with zeros, typically used for padding data arrays where cells on the edges are empty and not present in the data frame.

#### Syntax

```python
def pad_with_zeros(vector, pad_width, iaxis, kwargs):
```

#### Parameters

- `vector`: The array or vector to be padded with zeros.
- `pad_width`: A tuple specifying the number of zeros to pad at the beginning and end of the `vector`. The tuple format is `(pad_start, pad_end)`, where `pad_start` is the number of zeros to add at the start of the vector, and `pad_end` is the number of zeros to add at the end.
- `iaxis`: The axis along which padding is to be applied. For a vector, this is typically the only axis (axis 0).
- `kwargs`: Additional keyword arguments. This parameter is present for compatibility with padding functions but typically does not need to be used.

#### Returns

- The function modifies the input `vector` in place and does not return a separate value.

#### Example

```python
import numpy as np
from pharmbio_package.pharmbio.visualization.plots import pad_with_zeros

# Example vector
vector = np.array([1, 2, 3, 4, 5])

# Pad with two zeros at the start and three zeros at the end
pad_with_zeros(vector, (2, 3), 0, {})

print(vector)
# Output will be an array padded with zeros: [0, 0, 1, 2, 3, 4, 5, 0, 0, 0]
```