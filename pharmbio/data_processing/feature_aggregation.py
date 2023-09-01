import polars as pl
import importlib


def aggregate_morphology_data_cpu(
    df, columns_to_aggregate, groupby_columns, aggregation_function="mean"
):
    grouped = df.lazy().groupby(groupby_columns)
    retain_cols = [c for c in df.columns if c not in columns_to_aggregate]
    retained_metadata_df = df.lazy().select(retain_cols)

    # Aggregate only the desired columns.
    agg_exprs = [
        getattr(pl.col(col), aggregation_function)().alias(col)
        for col in columns_to_aggregate
    ]

    # Execute the aggregation.
    agg_df = grouped.agg(agg_exprs)
    agg_df = agg_df.join(retained_metadata_df, on=groupby_columns, how="left")

    return agg_df.sort(groupby_columns).collect()


def aggregate_morphology_data_gpu(
    df, columns_to_aggregate, groupby_columns, aggregation_function="mean"
):
    try:
        if client is None:
            LocalCUDACluster = importlib.import_module("dask_cuda").LocalCUDACluster
            Client = importlib.import_module("dask.distributed").Client
            dask = importlib.import_module("dask")
            with dask.config.set(jit_unspill=True):
                cluster = LocalCUDACluster(n_workers=4, device_memory_limit="2GB")
                client = Client(cluster)
        dd = importlib.import_module("dask.dataframe")
        np = importlib.import_module("numpy")

        # Check for special case where 'mean' should map to 'nanmean'
        if aggregation_function == "mean":
            agg_func = np.nanmean
        elif aggregation_function == "median":
            agg_func = np.nanmedian
        else:
            agg_func = getattr(np, aggregation_function)

        agg_dict = {col: agg_func for col in columns_to_aggregate}

        # Convert the Polars DataFrame to a Dask DataFrame
        # The number of partitions can be adjusted depending on your needs
        ddf = dd.from_pandas(df.to_pandas(), npartitions=4)
        agg_ddf = ddf.groupby(groupby_columns).agg(agg_dict).reset_index()

        sorted_ddf = agg_ddf.compute().sort_values(by=groupby_columns)

        return pl.from_arrow(sorted_ddf.to_arrow())

    except ImportError as e:
        raise ImportError(
            "Dask-CUDA is not available. Please install it to use GPU acceleration."
        ) from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e
