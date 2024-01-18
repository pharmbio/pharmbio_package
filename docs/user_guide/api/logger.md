### `set_logger_level(level)`

Sets the logger's level to the specified logging level.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/logger.py#L7)

```python
def set_logger_level(level: str):
```

#### Parameters

- `level` (str): The desired logging level. Accepted values are 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

#### Raises

- `ValueError`: Raised if an invalid log level is provided.

#### Examples

```python
set_logger_level('DEBUG')  # Sets the logging level to DEBUG
set_logger_level('INFO')   # Sets the logging level to INFO
```

### `log_debug(message)`

Logs a debug message.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/logger.py#L21)

```python
def log_debug(message: str):
```

#### Parameters

- `message` (str): The message to be logged at the DEBUG level.

#### Examples

```python
log_debug('Debugging started')  # Logs a debug message
```

### `log_info(message)` 

Logs an informational message.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/logger.py#L24)

```python
def log_info(message: str):
```

#### Parameters

- `message` (str): The message to be logged at the INFO level.

#### Examples

```python
log_info('Process completed successfully')  # Logs an informational message
```

### `log_warning(message)`

Logs a warning message.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/logger.py#L27)

```python
def log_warning(message: str):
```

#### Parameters

- `message` (str): The message to be logged at the WARNING level.

#### Examples

```python
log_warning('Memory usage is high')  # Logs a warning message
```


### `log_error(message)`

Logs an error message.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/logger.py#L30)

```python
def log_error(message: str):
```

#### Parameters

- `message` (str): The message to be logged at the ERROR level.

#### Examples

```python
log_error('Failed to connect to the database')  # Logs an error message
```

### `log_critical(message)`

Logs a critical message.

#### Syntax [[source]](https://github.com/pharmbio/pharmbio_package/blob/3cb9c60ec40851432f19ce7ecc5453e5f0b6ff1e/pharmbio/logger.py#L33)

```python
def log_critical(message: str):
```

#### Parameters

- `message` (str): The message to be logged at the CRITICAL level.

#### Examples

```python
log_critical('System failure: unable to recover')  # Logs a critical message
```
