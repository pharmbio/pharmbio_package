This Python configuration file (`config.py`) is part of the `pharmbio`, designed for managing various settings and parameters related to logging, database connections, data schemas, and quality control in a biomedical or pharmaceutical research context.

### Logging Level Setting
- **Description**: Defines the logging level for the application.
- **Variable**: `LOGGING_LEVEL`
- **Type**: `logging` (module from Python's standard library)
- **Usage**: Set to `logging.DEBUG` for detailed debugging information. Can be changed to other levels like `INFO`, `WARNING`, `ERROR`, etc.

### Database Connection Setting
- **Description**: Manages the Database URI connection settings.
- **Variable**: `DB_URI`
- **Type**: `string`
- **Usage**: The URI is stored as an environment variable for security reasons. It can be set in a Jupyter notebook, using the os.environ module, or as a system environment variable in bash.

### Database Schema
- **Description**: Describes the schema for the experiment metadata and plate layout in the database.
- **Variables**: `DATABASE_SCHEMA`, `PLATE_LAYOUT_INFO`
- **Type**: `dict`, `list`
- **Usage**: Outlines the structure and column names for the experiment metadata and plate layout tables.

### Image Quality Metadata Schema
- **Description**: Defines metadata type for image quality.
- **Variable**: `IMAGE_QUALITY_METADATA_TYPE`
- **Type**: `string`
- **Usage**: Used to specify the metadata type for image quality data, typically retrieved from ImageDB.

### Image Quality Module Data
- **Description**: Specifies file prefix for image quality data files.
- **Variable**: `IMAGE_QUALITY_FILE_PREFIX`
- **Type**: `string`
- **Usage**: Indicates the prefix for raw files containing image quality data.

### Cell Morphology Metadata Schema
- **Description**: Defines metadata type for cell morphology data.
- **Variable**: `CELL_MORPHOLOGY_METADATA_TYPE`
- **Type**: `string`
- **Usage**: Used to specify the metadata type for cell morphology data files.

### Metadata Columns in Image Quality and Morphology File
- **Description**: Lists the metadata columns used in image quality and morphology data files.
- **Variables**: `METADATA_ACQID_COLUMN`, `METADATA_BARCODE_COLUMN`, `METADATA_WELL_COLUMN`, `METADATA_SITE_COLUMN`, `METADATA_IMAGE_NUMBER_COLUMN`
- **Type**: `string`
- **Usage**: Identifies specific metadata columns in the data files for referencing acquisition, barcode, well, site, and image number.

### Object Morphology Data File
- **Description**: Details the configuration for object morphology data files.
- **Variables**: `OBJECT_FILE_NAMES`, `OBJECT_ID_COLUMN`, `OBJECT_PARENT_CELL_COLUMN`, `CELL_CYTOPLASM_COUNT_COLUMN`, `CELL_NUCLEI_COUNT_COLUMN`
- **Type**: `list`, `string`
- **Usage**: Specifies file names and column names for data related to object morphology, such as cell nuclei and cytoplasm.

### Image and Cell ID Construction
- **Description**: Constructs unique identifiers for images and cells.
- **Variables**: `IMAGE_ID_COLUMN_NAME`, `CELL_ID_COLUMN_NAME`, `CONSTRUCTING_IMAGE_ID`, `CONSTRUCTING_CELL_ID`
- **Type**: `string`, `polars` expression
- **Usage**: Combines various metadata fields to create unique identifiers for images and cells.

### Aggregation Method for Each Level
- **Description**: Defines aggregation methods for different levels (cell, site, well, etc.).
- **Variable**: `AGGREGATION_METHOD_DICT`
- **Type**: `dict`
- **Usage**: Specifies the aggregation method (mean, median, sum, etc.) for different levels of data analysis.

### Grouping Column Map
- **Description**: Maps aggregation levels to their respective grouping columns.
- **Variable**: `GROUPING_COLUMN_MAP`
- **Type**: `dict`
- **Usage**: Details the columns used for grouping data at different levels (cell, site, well, etc.).

### QC Modules Setting
- **Description**: Specifies default quality control modules to consider.
- **Variable**: `DEFAULT_QC_MODULES`
- **Type**: `set`
- **Usage**: Lists the default modules used for quality control assessment.

### Plot Discrete Color
- **Description**: Provides color settings for plots.
- **Variable**: `COLORS`
- **Type**: `plotly.express.colors`
- **Usage**: Defines a set of colors from Plotly's qualitative Set1 for use in data visualizations.


!!! Notes
    - **Security**: Care should be taken with `DB_URI` to ensure that database connections are secure.
    - **Flexibility**: The configuration allows for customization of data schemas, aggregation methods, and quality control modules, making it adaptable to various research needs.
    - **Dependencies**: The configuration relies on external libraries like `logging`, `os`, `polars`, and `plotly`.