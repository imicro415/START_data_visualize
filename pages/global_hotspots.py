import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px

dash.register_page(__name__, path="/global", name="Global Hotspots")

df = pd.read_csv("terrorism.csv", low_memory=False)
year_min = int(df["iyear"].min())
year_max = int(df["iyear"].max())

layout = html.Div(
    [
        html.H1("Global Terrorism Hotspots"),
        html.Div(
            [
                html.Label("Year Range"),
                dcc.RangeSlider(
                    id="global-year-range",
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
        dcc.Graph(id="global-map"),
        dcc.Graph(id="global-top-countries"),
    ],
    style={"padding": "0 40px 40px"},
)


@callback(
    Output("global-map", "figure"),
    Output("global-top-countries", "figure"),
    Input("global-year-range", "value"),
)
def update_global(year_range):
    filtered = df[df["iyear"].between(year_range[0], year_range[1])]

    by_country = filtered.groupby("country_txt").size().reset_index(name="incidents")
    fig1 = px.choropleth(
        by_country,
        locations="country_txt",
        locationmode="country names",
        color="incidents",
        title="Attack Density by Country",
        color_continuous_scale="Reds",
        template="plotly_dark",
    )
    fig1.update_layout(geo=dict(bgcolor="#1a1a2e"), paper_bgcolor="#16213e")
    fig1.update_layout(
        coloraxis_colorbar=dict(
            title="Incidents",
            tickformat=",",
            ##thickness=15,
            ##len=0.5,
            title_font=dict(size=13, color="#e0e0e0"),
            tickfont=dict(color="#e0e0e0"),
        )
    )
    fig1.update_traces(
        hovertemplate="<b>%{location}</b><br>Incidents: %{z:,}<extra></extra>"
    )

    top_countries = by_country.sort_values("incidents", ascending=False).head(20)
    fig2 = px.bar(
        top_countries,
        x="incidents",
        y="country_txt",
        orientation="h",
        title="Top 20 Countries by Incident Count",
        labels={"country_txt": "Country", "incidents": "Incidents"},
        template="plotly_dark",
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    fig2.update_traces(hovertemplate="<b>%{y}</b><br>Incidents: %{x:,}<extra></extra>")
    return fig1, fig2
