import polars as pl
import pandas as pd
import plotly.figure_factory as ff
import plotly.subplots as sp
import numpy as np
from typing import Union, List, Dict


def plate_heatmap(
    df: Union[pl.DataFrame, pd.DataFrame],
    plate_names: List[str] = None,
    subplot_num_columns: int = 2,
    plot_size: int = 400,
    measurement: str = "Count_nuclei",
    plate_well_columns: Dict[str, str] = {
        "plates": "Metadata_Barcode",
        "wells": "Metadata_Well",
    },
):
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    wells = (
        df.select("Metadata_Well")
        .unique()
        .sort(by="Metadata_Well")
        .to_series()
        .to_list()
    )
    rows = sorted(list({w[0] for w in wells}))
    columns = sorted(list({w[1:] for w in wells}))

    if plate_names is None:
        try:
            plate_names = (
                df.select(plate_well_columns["plates"])
                .unique()
                .sort(by=plate_well_columns["plates"])
                .to_series()
                .to_list()
            )
            print(plate_names)
        except Exception:
            print("Plate names is not specified")
            plate_names = []

    # Define the font ratio and number of rows for the grid
    font_ratio = plot_size / 400
    subplot_num_rows = -(
        -len(plate_names) // subplot_num_columns
    )  # Ceiling division to get number of rows needed

    titles = [f"{measurement} for {name} " for name in plate_names]

    # Create a subplot with subplot_num_rows rows and subplot_num_columns columns
    fig = sp.make_subplots(
        rows=subplot_num_rows,
        cols=subplot_num_columns,
        subplot_titles=titles,
    )

    for index, plate in enumerate(plate_names):
        plate_data = df.filter(pl.col(plate_well_columns["plates"]) == plate)
        heatmap_data = []
        heatmap_data_annot = []
        for row in rows:
            heatmap_row = []
            heatmap_row_annot = []
            for column in columns:
                well = row + column
                count_nuclei = plate_data.filter(
                    pl.col(plate_well_columns["wells"]) == well
                )[measurement].to_numpy()

                if count_nuclei.size == 0:
                    well_nuclei_count = 0
                else:
                    well_nuclei_count = (
                        np.mean(count_nuclei).round(decimals=0).astype(int)
                    )

                heatmap_row.append(well_nuclei_count)
                heatmap_row_annot.append(f"{well}: {well_nuclei_count}")
            heatmap_data.append(heatmap_row)
            heatmap_data_annot.append(heatmap_row_annot)

        # Calculate the subplot row and column indices
        subplot_row = index // subplot_num_columns + 1
        subplot_col = index % subplot_num_columns + 1

        heatmap = ff.create_annotated_heatmap(
            heatmap_data,
            x=[str(i + 1) for i in range(24)],
            y=rows,
            annotation_text=heatmap_data,
            colorscale="OrRd",
            hovertext=heatmap_data_annot,
            hoverinfo="text",
        )

        # Add the heatmap to the subplot
        fig.add_trace(heatmap.data[0], row=subplot_row, col=subplot_col)

    # Update x and y axes properties
    for i in fig["layout"]["annotations"]:
        i["font"] = dict(size=12 * font_ratio)
    fig.update_xaxes(tickfont=dict(size=10 * font_ratio), nticks=48, side="bottom")
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    # fig.update_yaxes(tickfont=dict(size=10*font_ratio))

    # Add the new lines here to adjust annotation positions
    for ann in fig.layout.annotations:
        ann.update(y=ann.y + 0.02)

    fig.update_layout(
        height=plot_size * subplot_num_rows,
        width=plot_size * 1.425 * subplot_num_columns,
    )
    fig.show()
