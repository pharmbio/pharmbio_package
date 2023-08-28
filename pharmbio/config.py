# ---------------------------------------------------------------------------- #
#                             LOGGING LEVEL SETTING                            #
# ---------------------------------------------------------------------------- #
import logging

LOGGING_LEVEL = logging.DEBUG

# ---------------------------------------------------------------------------- #
#                         DATABASE CONNECTION SETTING                          #
#  For sequrity reason the URI address is defined as an environment variable   #
#  and should be defined by user like so:                                      #
#                                                                              #
#  in Jupyter notbooke:                                                        #
#   %env DB_URI=URI_ADDRESS                                                    #
#                                                                              #
#  or using os environ module:                                                 #
#    import os                                                                 #
#    os.environ["DB_URI"] = "URI_ADDRESS"                                      #
#                                                                              #
#  or simply add it to system in bash command line:                            #
#     export DB_URI=URI_ADDRESS                                                #
# ---------------------------------------------------------------------------- #
import os

DB_URI = os.environ.get("DB_URI")

# ---------------------------------------------------------------------------- #
#                                DATABASE SCHEMA                               #
# ---------------------------------------------------------------------------- #

EXPERIMENT_METADATA_TABLE_NAME_ON_DB = "image_analyses_per_plate"
EXPERIMENT_NAME_COLUMN = "project"
EXPERIMENT_PLATE_BARCODE_COLUMN = "plate_barcode"
EXPERIMENT_PLATE_ACQID_COLUMN = "plate_acq_id"
EXPERIMENT_ANALYSIS_ID_COLUMN = "analysis_id"
EXPERIMENT_ANALYSIS_DATE_COLUMN = "analysis_date"
EXPERIMENT_RESULT_DIRECTORY_COLUMN = "results"

# ----------------------- IMAGE QUALITY METADATA SCHEMA ---------------------- #
#  The dataframe that include the metadata for the image quality data and      #
#  refrence to the image quality data file and is retrived from the ImageDB.   #
# ---------------------------------------------------------------------------- #

IMAHGE_QUALITY_METADATA_TYPE = "'cp-qc'"

# ------------------------- IMAGE QUALITY MODULE DATA ------------------------ #
#  The dataframe that include the image quality data produced by cellprofiler  #
#  for each plate and retrived from csv/parquet file in the result directory.  #
# ---------------------------------------------------------------------------- #

IMAGE_QUALITY_FILE_PREFIX = "qcRAW_images_"

# ---------------------- CELL MORPHOLOGY METADATA SCHEMA --------------------- #
#  The dataframe that include the metadata for the cell morphology data and    #
#  refrence to the cell morphology data files and is retrived from the ImageDB.#
# ---------------------------------------------------------------------------- #

CELL_MORPHOLOGY_METADATA_TYPE = "'cp-features'"