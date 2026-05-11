import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.SLATE,
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&display=swap",
    ],
)

navbar = html.Div(
    [
        dcc.Link("Global Terrorism Database", href="/", style={"fontWeight": "600", "fontSize": "1.1rem", "textDecoration": "none", "color": "inherit"}),
        html.Div(
            [
                dcc.Link("US Attacks", href="/us", style={"marginRight": "24px"}),
                dcc.Link("Global Hotspots", href="/global", style={"marginRight": "24px"}),
                dcc.Link("Attack Methods", href="/methods", style={"marginRight": "24px"}),
                dcc.Link("Casualties", href="/casualties"),
            ]
        ),
    ],
    style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "padding": "16px 40px",
        "borderBottom": "1px solid #333",
        "marginBottom": "20px",
    },
)

app.layout = html.Div([navbar, dash.page_container])

if __name__ == "__main__":
    app.run(debug=True)
