import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px

dash.register_page(__name__, path="/us", name="US Attacks")

df = pd.read_csv("terrorism.csv", low_memory=False)
us = df[df["country_txt"] == "United States"].copy()
attack_types = sorted(us["attacktype1_txt"].dropna().unique())

layout = html.Div(
    [
        html.H1("US Terrorist Attacks Over Time"),
        html.Div(
            [
                html.Label("Attack Type"),
                dcc.Dropdown(
                    id="us-attack-type",
                    options=[{"label": "All", "value": "All"}]
                    + [{"label": a, "value": a} for a in attack_types],
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
                    id="us-year-range",
                    min=int(us["iyear"].min()),
                    max=int(us["iyear"].max()),
                    step=1,
                    value=[int(us["iyear"].min()), int(us["iyear"].max())],
                    marks={y: str(y) for y in range(int(us["iyear"].min()), int(us["iyear"].max()) + 1, 5)},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={"marginBottom": "40px"},
        ),
        dcc.Graph(id="us-attacks-over-time"),
        dcc.Graph(id="us-breakdown-chart"),
    ],
    style={"padding": "0 40px 40px"},
)


@callback(
    Output("us-attacks-over-time", "figure"),
    Output("us-breakdown-chart", "figure"),
    Input("us-attack-type", "value"),
    Input("us-year-range", "value"),
)
def update_charts(attack_type, year_range):
    filtered = us[us["iyear"].between(year_range[0], year_range[1])]
    if attack_type != "All":
        filtered = filtered[filtered["attacktype1_txt"] == attack_type]

    by_year = filtered.groupby("iyear").size().reset_index(name="incidents")
    fig1 = px.line(
        by_year, x="iyear", y="incidents",
        title="Incidents per Year",
        labels={"iyear": "Year", "incidents": "Incidents"},
        markers=True, template="plotly_dark",
    )

    by_group = (
        filtered.groupby("gname").size()
        .reset_index(name="incidents")
        .sort_values("incidents", ascending=False)
        .head(15)
    )
    fig2 = px.bar(
        by_group, x="incidents", y="gname", orientation="h",
        title="Top 15 Groups (selected range)",
        labels={"gname": "Group", "incidents": "Incidents"},
        template="plotly_dark",
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig1, fig2
