import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px

dash.register_page(__name__, path="/casualties", name="Casualties")

df = pd.read_csv("terrorism.csv", low_memory=False)
year_min = int(df["iyear"].min())
year_max = int(df["iyear"].max())
countries = sorted(df["country_txt"].dropna().unique())

layout = html.Div(
    [
        html.H1("Casualties & Severity"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="cas-country",
                            options=[{"label": "All", "value": "All"}]
                            + [{"label": c, "value": c} for c in countries],
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
                            id="cas-year-range",
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
        dcc.Graph(id="cas-over-time"),
        dcc.Graph(id="deadliest-incidents"),
    ],
    style={"padding": "0 40px 40px"},
)


@callback(
    Output("cas-over-time", "figure"),
    Output("deadliest-incidents", "figure"),
    Input("cas-country", "value"),
    Input("cas-year-range", "value"),
)
def update_casualties(country, year_range):
    filtered = df[df["iyear"].between(year_range[0], year_range[1])].copy()
    if country != "All":
        filtered = filtered[filtered["country_txt"] == country]

    filtered["nkill"] = pd.to_numeric(filtered["nkill"], errors="coerce").fillna(0)
    filtered["nwound"] = pd.to_numeric(filtered["nwound"], errors="coerce").fillna(0)

    by_year = filtered.groupby("iyear")[["nkill", "nwound"]].sum().reset_index()
    fig1 = px.area(
        by_year, x="iyear", y=["nkill", "nwound"],
        title="Killed vs. Wounded Over Time",
        labels={"iyear": "Year", "value": "Count", "variable": "Type"},
        template="plotly_dark",
    )
    fig1.for_each_trace(lambda t: t.update(name="Killed" if t.name == "nkill" else "Wounded"))

    deadliest = (
        filtered.nlargest(20, "nkill")[["iyear", "country_txt", "city", "gname", "attacktype1_txt", "nkill", "nwound"]]
        .rename(columns={
            "iyear": "Year", "country_txt": "Country", "city": "City",
            "gname": "Group", "attacktype1_txt": "Attack Type",
            "nkill": "Killed", "nwound": "Wounded",
        })
    )
    fig2 = px.bar(
        deadliest, x="Killed", y="City", orientation="h",
        title="20 Deadliest Incidents (selected range)",
        hover_data=["Year", "Country", "Group", "Attack Type", "Wounded"],
        template="plotly_dark",
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig1, fig2
