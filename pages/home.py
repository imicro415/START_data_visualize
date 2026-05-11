import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path="/", name="Home")

layout = html.Div(
    [
        html.H1("Global Terrorism Database Visualization"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("About the Data"),
                        html.P([
                            "The data visualized here is drawn from the Global Terrorism Database (GTD), a comprehensive "
                            "and methodologically rigorous longitudinal dataset documenting incidents of domestic and "
                            "international terrorism. Developed by the National Consortium for the Study of Terrorism and "
                            "Responses to Terrorism (START), the GTD is designed to support researchers and analysts in "
                            "advancing the understanding of terrorism as a global phenomenon. It is specifically constructed "
                            "to be compatible with modern quantitative analytic methods used across the social and "
                            "computational sciences.",
                            html.Br(), html.Br(),
                            "The visualizations presented here represent a curated subset of the full dataset and serve as "
                            "a proof of concept for exploring GTD data interactively."
                        ]),
                        html.H2("How To Interact With the Data"),
                        html.P([
                            "To get the most out of the data presented on this site, it is recommended that you first "
                            "consult the GTD Codebook, available via the link below. The codebook details how incidents "
                            "are defined, collected, and categorized, providing the context necessary to interpret the "
                            "visualizations accurately. Each data point reflects a specific set of criteria, and "
                            "understanding how incidents are classified will greatly inform how you read the charts "
                            "and figures presented here."
                        ]),
                        html.H2("Citations"),
                        html.Ul(
                            [
                                html.Li(
                                    "National Consortium for the Study of Terrorism and Responses to Terrorism (START), "
                                    "University of Maryland. (2022). The Global Terrorism Database (GTD) "
                                    "[Data file]. Retrieved from https://www.start.umd.edu/gtd"
                                ),
                            ]
                        ),
                        html.H2("START Terrorism Database"),
                        html.Div(
                            [
                                dcc.Link("Link to START", href="https://www.start.umd.edu/data-tools/GTD", target="_blank", style={"marginRight": "24px"}),
                            ]
                        ),
                        html.Br(),
                    ],
                    style={"flex": "1"},
                ),
                html.Img(
                    src="/assets/hero.png",
                    style={"width": "100%", "borderRadius": "8px", "objectFit": "cover"},
                ),
            ],
            className="home-hero",
        ),
    ],
    style={"padding": "0 40px 40px"},
)

