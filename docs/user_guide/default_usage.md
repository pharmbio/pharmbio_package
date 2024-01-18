# Default Usage

## Looking up the experiment in the database with name

The `get_projects_list` function in the `pharmbio.dataset.experiment` module is designed for easy retrieval of project lists from your database. It's a straightforward function that can be used to get a complete list of projects or to filter them based on a keyword.

To use the function, simply call it without any arguments to get a full list of projects:

```python
from pharmbio.dataset.experiment import get_projects_list

all_projects = get_projects_list()
print(all_projects)
```

If you need to filter the list, provide a keyword to the `lookup` parameter. This search is not case-sensitive and will return any project that contains the keyword, regardless of its position in the name.

Example with a lookup filter:

```python
filtered_list = get_projects_list(lookup='aros')
print(filtered_list)
# Output might include projects like 'AROS-CP', 'AROS-Reproducibility-MoA-Full'
```

## Accessing Image Quality Data

After finding the full name of the experiment, the next step is to pull quality control data from the database. This is essential for pre-analysis steps, allowing you to validate the quality of your images before further processing. Here is how you do this:

```python
from pharmbio.dataset.image_quality import get_image_quality_ref, get_image_quality_data

# Retrieve a reference DataFrame based on the study name
qc_ref_df = get_image_quality_ref('AROS-Reproducibility-MoA-Full')

# Get the actual quality control data based on the reference DataFrame
qc_df = get_image_quality_data(qc_ref_df)
```

## Flagging Outlier Images

Once you have obtained the quality control data, you can flag outlier images based on pre-defined criteria. Outliers could be indicative of issues like focusing errors, staining inconsistencies, or other anomalies that may adversely affect the images. This step will just add some extra columns to dataframe which indicate which image (row) has poor quality. Here's how to flag these outliers using the `flag_outlier_images` function:

```python
from pharmbio.data_processing.quality_control import flag_outlier_images

# Flag outlier images based on the default setting
flagged_qc_df = flag_outlier_images(qc_df)
```

## Retrieving Cell Morphology Data

You can also proceed to obtain cell morphology data for your study. This is crucial for downstream joining of two dataframes (cell phenotype and its flagged image quality). This is how you do this:

```python
from pharmbio.dataset.cell_morphology import get_cell_morphology_ref, get_cell_morphology_data

# Retrieve a reference DataFrame based on the study name
cp_ref_df = get_cell_morphology_ref("AROS-Reproducibility-MoA-Full")

# Get the actual cell morphology data based on the reference DataFrame
cp_df = get_cell_morphology_data(cp_ref_df)
```

## Merging Image Quality Data and Cell Morphology Data

...