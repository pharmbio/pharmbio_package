# Installation

## From Terminal

The `pharmbio` package is available on PyPI and can be easily installed using pip:

```bash
pip install pharmbio
```

To update the package to the latest version, use:

```bash
pip install -U pharmbio
```

Alternatively, you can install the package directly from our GitHub repository:

```bash
pip install git+https://github.com/pharmbio/pharmbio_package.git
```
## From Jupyter Notebook

If you want to install or update the package within a Jupyter Notebook, you have two options:

**1- Using !pip**

Run a cell with the following command:

```bash
!pip install pharmbio
```

**2- Using %pip**

Alternatively, you can use the %pip magic command for a more environment-aware installation:

```
%pip install pharmbio
```

!!! warning "When using Jupyter notebook to install a package"

    - ! is for shell commands that are unaware of your Python environment.
    - % is for IPython magic commands that are often Python-aware.

    When you use `%pip` in a Jupyter Notebook, the package will be installed in the same Python environment where the Jupyter Notebook kernel is running.
    Using `%pip` ensures that you don't get confused about which Python environment you're installing the package into, especially useful when you have multiple Python environments on your system.