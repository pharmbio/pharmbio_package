## `pharmbio.database.queries`

The primary purpose of this module is to create and execute SQL queries for retrieving specific types of data from a database.

### `experiment_name_sql_query()` 

Executes a SQL query to retrieve experiment names from a specified table in the database.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/database/queries.py#L4)

```python
def experiment_name_sql_query(experiment_name: str, table_name_on_db: str) -> str:
```

#### Parameters

- `experiment_name` (str): Name of the experiment column to select.
- `table_name_on_db` (str): Name of the table to query in the database.

#### Returns

- `str`: SQL query string to retrieve experiment names.

### `experiment_metadata_sql_query()`

Executes a SQL query to retrieve metadata for a specific experiment from the database.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/database/queries.py#L32)

```python
def experiment_metadata_sql_query(name: str, db_schema: dict, experiment_type: str) -> str:
```

#### Parameters

- `name` (str): Name of the experiment to search for.
- `db_schema` (dict): A dictionary containing the names of the database schema tables and columns. Keys should include  `'EXPERIMENT_METADATA_TABLE_NAME_ON_DB'`, `'EXPERIMENT_NAME_COLUMN'`, `'EXPERIMENT_ANALYSIS_DATE_COLUMN'`, `'EXPERIMENT_PLATE_BARCODE_COLUMN'`, `'EXPERIMENT_PLATE_ACQID_COLUMN'`, and `'EXPERIMENT_ANALYSIS_ID_COLUMN'`, each mapped to their corresponding names in the database.
- experiment_type (str): The type of experiment to filter the query by. This allows the query to return metadata for a specific type of experiment. Valid values are "cp-qc" for quality control and "cp-features" for cell features.

#### Returns

Returns

- `str`: SQL query string to retrieve experiment names.


#### Example

```python
name = 'my_experiment'
db_schema = {
    'EXPERIMENT_METADATA_TABLE_NAME_ON_DB': 'experiment_table',
    'EXPERIMENT_NAME_COLUMN': 'name',
    'EXPERIMENT_ANALYSIS_DATE_COLUMN': 'analysis_date',
    'EXPERIMENT_PLATE_BARCODE_COLUMN': 'plate_barcode',
    'EXPERIMENT_PLATE_ACQID_COLUMN': 'plate_acqid',
    'EXPERIMENT_ANALYSIS_ID_COLUMN': 'analysis_id'
}
experiment_type = 'cp-features'

query = experiment_metadata_sql_query(name, db_schema, experiment_type)
print(query)
```

### `plate_layout_sql_query`()

Executes a SQL query to retrieve plate layout information from the database based on the given plate barcode.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/database/queries.py#L71)

```python
def plate_layout_sql_query(db_schema: dict, plate_barcode: str) -> str:
```

#### Parameters

- `db_schema` (dict): A dictionary containing the names of the database schema tables. This should include keys like `'PLATE_LAYOUT_TABLE_NAME_ON_DB'`, `'PLATE_LAYOUT_BARCODE_COLUMN'`, and `'PLATE_COMPOUND_NAME_COLUMN'` with their corresponding table and column names in the database.
- `plate_barcode` (str): The barcode identifier of the plate for which layout information is being queried.

#### Returns

- `str`: A string representing the SQL query. This query is structured to select plate layout information from the specified database schema based on the provided plate barcode.

#### Example

```python
db_schema = {
    'PLATE_LAYOUT_TABLE_NAME_ON_DB': 'plate_v1',
    'PLATE_LAYOUT_BARCODE_COLUMN': 'barcode',
    'PLATE_COMPOUND_NAME_COLUMN': 'batch_id'
}
plate_barcode = 'ABC123'

query = plate_layout_sql_query(db_schema, plate_barcode)
```