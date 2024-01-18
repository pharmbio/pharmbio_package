This module contains utility functions for file handling, data normalization, GPU detection, and GPU information retrieval in the `pharmbio` package.

### `get_file_extension()`

Returns the file extension for the given file path (directory + filename).

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/utils.py#L12)

```python
def get_file_extension(file_path_name: str) -> Optional[str]:
```

#### Parameters

- `file_path_name` (str): The path and name of the file without an extension.

#### Returns

- `Optional[str]`: The file extension if the file exists with any of the possible extensions [".parquet", ".csv", ".tsv"], otherwise `None`.

#### Example

```python
# Checking example.csv in the data directory
filename = "data/example"
extension = get_file_extension(file_path_name)
print(extension)
# Output: ".csv"
```

### `read_file()`

Reads a file with the specified filename and extension and returns a DataFrame.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/utils.py#L38)

```python
def read_file(filename: str, extension: str) -> Union[pl.DataFrame, None]:
```

#### Parameters

- `filename` (str): The name of the file to be read.
- `extension` (str): The extension of the file.

#### Returns

- `Union[pl.DataFrame, None]`: The DataFrame read from the file, or `None` if the extension is not supported.

#### Example

```python
filename = "data"
extension = ".parquet"
df = read_file(filename, extension)
print(df)
```

### `normalize_df()`

Normalizes the values in the DataFrame using the specified normalization method.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/utils.py#L72)

```python
def normalize_df(df: Union[pl.DataFrame, pd.DataFrame], method: Literal["zscore", "minmax"] = "zscore") -> pl.DataFrame:
```

#### Parameters

- `df` (Union[pl.DataFrame, pd.DataFrame]): The input DataFrame to be normalized.
- `method` (Literal["zscore", "minmax"], optional): The normalization method to be applied. Defaults to "zscore".

#### Returns

- `pl.DataFrame`: The normalized DataFrame.

#### Example

```python
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8],
    'C': [9, 10, 11, 12]
})
normalized_df = normalize_df(df, method='minmax')
print(normalized_df)
```

### `pretty_print_channel_dict()`

Prints the contents of a dictionary in a readable format for channel-related information.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/utils.py#L119)

```python
def pretty_print_channel_dict(d: Dict[str, Any]):
```

#### Parameters

- `d` (Dict[str, Any]): A dictionary containing channel-related information.

### `has_gpu()`

Checks if the system has a GPU available using the "nvidia-smi" command.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/utils.py#L128)

```python
def has_gpu() -> bool:
```

#### Returns

- `bool`: `True` if a GPU is available, `False` otherwise.

### `get_gpu_info()`

Retrieves GPU information including total memory and GPU count.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/utils.py#L142)

```python
def get_gpu_info() -> Tuple[Optional[int], Optional[int]]:
```

#### Returns

- `Tuple[Optional[int], Optional[int]]`: A tuple containing the total memory in MB and the number of GPUs.

#### Example

```python
total_memory, gpu_count = get_gpu_info()
print(f"Total Memory: {total_memory} MB")
print(f"Number of GPUs: {gpu_count}")
```