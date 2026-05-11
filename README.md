# Global Terrorism Database Visualization

An interactive data visualization web app built with Python and Plotly Dash, exploring a curated subset of the Global Terrorism Database (GTD) maintained by START at the University of Maryland.

## Pages

- **Home** — Overview of the project, data description, and link to START
- **US Attacks** — US terrorist incidents over time, filterable by attack type and year range
- **Global Hotspots** — Choropleth map and bar chart of attack density by country
- **Attack Methods** — Attack types over time and incidents by weapon type
- **Casualties** — Killed vs. wounded over time and the 20 deadliest incidents

## Setup

1. Clone the repo
2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Generate the dataset (requires the original Excel file from START):
   ```
   python parse.py
   ```
5. Run the app:
   ```
   python app.py
   ```

Open `http://127.0.0.1:8050` in your browser.

## Data

The dataset used is the Global Terrorism Database (GTD):

> National Consortium for the Study of Terrorism and Responses to Terrorism (START), University of Maryland. (2022). The Global Terrorism Database (GTD) [Data file]. Retrieved from https://www.start.umd.edu/gtd
