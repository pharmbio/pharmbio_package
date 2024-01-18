# Basic Usage

## 1- Setting the Database URI Environment Variable

You have two options for setting the database URI as an environment variable:

**Using Jupyter Notebook's %env Magic Command**

If you are using Jupyter Notebook, you can use the `%env` magic command to set environment variables within your notebook:

```python
%env DB_URI=your_database_uri_here
```

**Using Python's `os` Library**

Alternatively, you can use Python's built-in `os` library to set the environment variable in your script or notebook:

```python
import os
os.environ["DB_URI"] = "your_database_uri_here"
```

!!! Info "DB_URI"

    For security reasons, the actual URI is not disclosed in this documentation. You will need to replace `your_database_uri_here` with the actual URI that you should have received from your system administrator or through internal protocols.

## 2- Accessing Image Quality Data

After setting up your environment, the next step is to pull quality control data from the database. This is essential for pre-analysis steps, allowing you to validate the quality of your images before further processing. Here is a brief explanation of the code and its outputs for this part:

```python
from pharmbio.dataset.image_quality import get_image_quality_ref, get_image_quality_data

# Retrieve a reference DataFrame based on the study name
qc_ref_df = get_image_quality_ref('AROS-Reproducibility-MoA-Full')

# Get the actual quality control data based on the reference DataFrame
qc_df = get_image_quality_data(qc_ref_df)
```

## 3- Flagging Outlier Images

Once you have obtained the quality control data, you can flag outlier images based on pre-defined criteria. Outliers could be indicative of issues like focusing errors, staining inconsistencies, or other anomalies that may adversely affect the images. Here's how to flag these outliers using the `flag_outlier_images` function:

```python
from pharmbio.data_processing.quality_control import flag_outlier_images

# Flag outlier images based on the default setting
flagged_qc_df = flag_outlier_images(qc_df)
```

## 4- Retrieving Cell Morphology Data

You can also proceed to obtain cell morphology data for your study. This is crucial for downstream joining of two dataframes (cell phenotype and its image quality). Below is the code and its explanations:

```python
from pharmbio.dataset.cell_morphology import get_cell_morphology_ref, get_cell_morphology_data

# Retrieve a reference DataFrame based on the study name
cp_ref_df = get_cell_morphology_ref("AROS-Reproducibility-MoA-Full")

# Get the actual cell morphology data based on the reference DataFrame
cp_df = get_cell_morphology_data(cp_ref_df)
```

## 5- Merging Image Quality Data and Cell Morphology Data

...