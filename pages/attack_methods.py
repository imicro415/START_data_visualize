import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px

dash.register_page(__name__, path="/methods", name="Attack Methods")

df = pd.read_csv("terrorism.csv", low_memory=False)
year_min = int(df["iyear"].min())
year_max = int(df["iyear"].max())
regions = sorted(df["region_txt"].dropna().unique())

layout = html.Div(
    [
        html.H1("Attack Methods & Weapons"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Region"),
                        dcc.Dropdown(
                            id="methods-region",
                            options=[{"label": "All", "value": "All"}]
                            + [{"label": r, "value": r} for r in regions],
                            value="All",
                            clearable=False,
                        ),
                    ],
                    style={"width": "300px", "marginBottom": "20px"},
                ),
                html.Div(
                    [
                        html.Label("Year Range"),
                        dcc.RangeSlider(
                            id="methods-year-range",
                            min=year_min,
                            max=year_max,
                            step=1,
                            value=[year_min, year_max],
                            marks={y: str(y) for y in range(year_min, year_max + 1, 5)},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"marginBottom": "40px"},
                ),
            ]
        ),
        dcc.Graph(id="methods-over-time"),
        dcc.Graph(id="weapons-breakdown"),
    ],
    style={"padding": "0 40px 40px"},
)


@callback(
    Output("methods-over-time", "figure"),
    Output("weapons-breakdown", "figure"),
    Input("methods-region", "value"),
    Input("methods-year-range", "value"),
)
def update_methods(region, year_range):
    filtered = df[df["iyear"].between(year_range[0], year_range[1])]
    if region != "All":
        filtered = filtered[filtered["region_txt"] == region]

    by_type = (
        filtered.groupby(["iyear", "attacktype1_txt"])
        .size()
        .reset_index(name="incidents")
    )
    fig1 = px.line(
        by_type,
        x="iyear",
        y="incidents",
        color="attacktype1_txt",
        title="Attack Types Over Time",
        labels={
            "iyear": "Year",
            "incidents": "Incidents",
            "attacktype1_txt": "Attack Type",
        },
        template="plotly_dark",
    )

    by_weapon = (
        filtered.groupby("weaptype1_txt")
        .size()
        .reset_index(name="incidents")
        .sort_values("incidents", ascending=False)
    )
    fig2 = px.bar(
        by_weapon,
        x="incidents",
        y="weaptype1_txt",
        orientation="h",
        title="Incidents by Weapon Type",
        labels={"weaptype1_txt": "Weapon Type", "incidents": "Incidents"},
        template="plotly_dark",
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    fig2.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_type="log",
        xaxis_title="Incidents (logarithmic scale)",
    )

    return fig1, fig2
