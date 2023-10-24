# PHARMBIO
The `pharmbio` Python package serves as a toolkit developed for the Pharmaceutical Bioinformatics Research Group at Uppsala University, Sweden.

!!! note "Server Connection Dependency and Usage Constraints"

    Please note that the `pharmbio` package is tightly integrated with the data server and file repository infrastructure of the Pharmaceutical Bioinformatics Research Group at Uppsala University. As such, it is not designed to function outside of this specific server workflow. The package is optimized for use within the group's ecosystem and its full range of functionalities are only accessible when connected to the group's server environment. Users should deploy and utilize `pharmbio` with this critical dependency in mind.

## Introduction

 This package is engineered to enhance research workflows by offering a robust set of tools for data processing, quality control, and visualization. Specifically tailored for projects within the lab, the package facilitates seamless interactions with the group's data server and file repository. It specializes in handling 'cell painting' data, including both image and tabular formats, offering features from quality control on cellular images to in-depth analysis of cell phenotypes and chemical compound metadata. 
 
 By streamlining various lab tasks, `pharmbio` aims to set a standard, easy-to-implement workflow for all experiments run within the research group.

The `pharmbio` package is modular and designed for extensibility, making it well-suited for meeting the evolving needs of the research group. It incorporates state-of-the-art libraries and technologies to ensure efficiency.

## Installation

### From Terminal

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
### From Jupyter Notebook
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

