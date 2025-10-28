# app.py
# Dependencies: pip install dash==2.17.1 plotly>=5.22 pandas

from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css, assets_folder="assets")
app.title = "Gapminder Dashboard"

################### DATASET ####################################
gapminder_df = px.data.gapminder().rename(columns={
    "country": "Country",
    "continent": "Continent",
    "year": "Year",
    "pop": "Population",
    "lifeExp": "Life Expectancy",
    "gdpPercap": "GDP per Capita",
    "iso_alpha": "ISO Alpha Country Code"
})
gapminder_df["Year"] = gapminder_df["Year"].astype(int)
# 计算总 GDP（便于中国趋势分析）
gapminder_df["GDP"] = gapminder_df["Population"] * gapminder_df["GDP per Capita"]

#################### CHARTS ####################################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(gapminder_df.columns), align='left'),
        cells=dict(values=[gapminder_df[col] for col in gapminder_df.columns], align='left'))
    ])
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
    return fig

def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["Continent"] == continent) & (gapminder_df["Year"] == year)]
    filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)
    fig = px.bar(
        filtered_df,
        x="Country",
        y="Population",
        color="Country",
        title=f"Country Population for {continent} in {year}",
        text_auto=True
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["Continent"] == continent) & (gapminder_df["Year"] == year)]
    filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)
    fig = px.bar(
        filtered_df,
        x="Country",
        y="GDP per Capita",
        color="Country",
        title=f"Country GDP per Capita for {continent} in {year}",
        text_auto=True
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["Continent"] == continent) & (gapminder_df["Year"] == year)]
    filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)
    fig = px.bar(
        filtered_df,
        x="Country",
        y="Life Expectancy",
        color="Country",
        title=f"Country Life Expectancy for {continent} in {year}",
        text_auto=True
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df["Year"] == year]
    fig = px.choropleth(
        filtered_df,
        color=variable,
        locations="ISO Alpha Country Code",
        locationmode="ISO-3",
        color_continuous_scale="RdYlBu",
        hover_data=["Country", variable],
        title=f"{variable} Choropleth Map [{year}]"
    )
    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin={"l":0, "r":0})
    return fig

##################### WIDGETS ###################################
continents = sorted(gapminder_df["Continent"].unique().tolist())
years = sorted(gapminder_df["Year"].unique().tolist())

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia", clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=years, value=1952, clearable=False)

cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia", clearable=False)
year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952, clearable=False)

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia", clearable=False)
year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952, clearable=False)

year_map = dcc.Dropdown(id="year_map", options=years, value=1952, clearable=False)
var_map = dcc.Dropdown(
    id="var_map",
    options=["Population", "GDP per Capita", "Life Expectancy"],
    value="Life Expectancy",
    clearable=False
)

# 中国趋势页签用到的变量选择
china_vars = ["Population", "GDP per Capita", "Life Expectancy", "GDP"]
china_var_dd = dcc.Dropdown(id="china_var", options=china_vars, value="GDP", clearable=False)

##################### APP LAYOUT ###############################
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src="/assets/globe.png", style={"width": "44px", "height": "44px"}, className="me-2"),
            html.H1("Gapminder Dataset Analysis Dashboard", className="d-inline fw-bold m-0"),
            html.Img(src="/assets/chart.png", style={"width": "44px", "height": "44px"}, className="ms-2"),
        ], className="mb-2 d-flex justify-content-center align-items-center"),
        html.P("Explore global development data across continents and decades",
               className="text-muted text-center fs-5"),
        html.P([
            html.I(className="bi bi-link-45deg me-1"),
            "Reference site: ",
            html.A(
                "https://1234750zhanyipaulantony.pythonanywhere.com/",
                href="https://paulantonychen.pythonanywhere.com/",
                target="_blank",
                className="link-primary"
            )
        ], className="text-center mb-0"),
    ], className="text-center mb-3 p-3", style={"background": "#eaf2fb", "borderRadius": "12px"}),

    dcc.Tabs([
        dcc.Tab(
            label="📊 Dataset",
            children=[
                html.Br(),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4([html.I(className="bi bi-table me-2"), "Dataset Overview"], className="mb-1"),
                            html.P("All columns and records at a glance", className="text-muted mb-2")
                        ], className="card-header bg-white border-0 pb-0"),
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-lightbulb me-2 text-warning"),
                                html.Small("Scroll horizontally/vertically to explore the raw Gapminder table.")
                            ], className="text-muted mb-2"),
                            dcc.Graph(id="dataset", figure=create_table())
                        ], className="card-body pt-2"),
                    ], className="card shadow-sm")
                ], className="mb-4")
            ]
        ),

        dcc.Tab(
            label="👥 Population",
            children=[
                html.Br(),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4([html.I(className="bi bi-bar-chart-fill me-2"), "Population"], className="mb-1"),
                            html.P("Top 15 countries by population", className="text-muted mb-2")
                        ], className="card-header bg-white border-0 pb-0"),
                        html.Div([
                            html.Div([
                                html.Div(["Continent", cont_population], className="col-6"),
                                html.Div(["Year", year_population], className="col-6")
                            ], className="row g-2 mb-2"),
                            html.Div([
                                html.I(className="bi bi-lightbulb me-2 text-warning"),
                                html.Small("Use toolbar (top-right) to save PNG, zoom, or select.")
                            ], className="text-muted mb-2"),
                            dcc.Graph(id="population")
                        ], className="card-body pt-2"),
                    ], className="card shadow-sm")
                ], className="mb-4")
            ]
        ),

        dcc.Tab(
            label="💰 GDP",
            children=[
                html.Br(),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4([html.I(className="bi bi-currency-dollar me-2"), "GDP per Capita"], className="mb-1"),
                            html.P("Top 15 countries by GDP per capita", className="text-muted mb-2")
                        ], className="card-header bg-white border-0 pb-0"),
                        html.Div([
                            html.Div([
                                html.Div(["Continent", cont_gdp], className="col-6"),
                                html.Div(["Year", year_gdp], className="col-6")
                            ], className="row g-2 mb-2"),
                            html.Div([
                                html.I(className="bi bi-exclamation-circle me-2 text-warning"),
                                html.Small("Nominal values; cross-period comparisons may be misleading.")
                            ], className="text-muted mb-2"),
                            dcc.Graph(id="gdp")
                        ], className="card-body pt-2"),
                    ], className="card shadow-sm")
                ], className="mb-4")
            ]
        ),

        dcc.Tab(
            label="❤️ Life Expectancy",
            children=[
                html.Br(),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4([html.I(className="bi bi-activity me-2"), "Life Expectancy"], className="mb-1"),
                            html.P("Top 15 countries by life expectancy", className="text-muted mb-2")
                        ], className="card-header bg-white border-0 pb-0"),
                        html.Div([
                            html.Div([
                                html.Div(["Continent", cont_life_exp], className="col-6"),
                                html.Div(["Year", year_life_exp], className="col-6")
                            ], className="row g-2 mb-2"),
                            html.Div([
                                html.I(className="bi bi-info-circle me-2 text-primary"),
                                html.Small("Affected by public health, economy, conflicts, etc.")
                            ], className="text-muted mb-2"),
                            dcc.Graph(id="life_expectancy")
                        ], className="card-body pt-2"),
                    ], className="card shadow-sm")
                ], className="mb-4")
            ]
        ),

        dcc.Tab(
            label="🗺️ World Map",
            children=[
                html.Br(),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4([html.I(className="bi bi-map-fill me-2"), "World Distribution Map"], className="mb-1"),
                            html.P("Population / GDP per Capita / Life Expectancy by country", className="text-muted mb-2")
                        ], className="card-header bg-white border-0 pb-0"),
                        html.Div([
                            html.Div([
                                html.Div(["Variable", var_map], className="col-6"),
                                html.Div(["Year", year_map], className="col-6")
                            ], className="row g-2 mb-2"),
                            html.Div([
                                html.I(className="bi bi-lightbulb me-2 text-warning"),
                                html.Small("Drag/zoom the map. Try different years or variables if colors look close.")
                            ], className="text-muted mb-2"),
                            dcc.Graph(id="choropleth_map")
                        ], className="card-body pt-2"),
                    ], className="card shadow-sm")
                ], className="mb-4")
            ]
        ),

        # 新：中国增长趋势分析
        dcc.Tab(
            label="🇨🇳 China Trends",
            children=[
                html.Br(),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4([html.I(className="bi bi-graph-up-arrow me-2"), "China Growth Trends"], className="mb-1"),
                            html.P("Select an indicator to analyze China's long-term level and YoY growth", className="text-muted mb-2")
                        ], className="card-header bg-white border-0 pb-0"),
                        html.Div([
                            html.Div([
                                html.Div(["Indicator", china_var_dd], className="col-6"),
                            ], className="row g-2 mb-3"),

                            html.Div([
                                html.Div([
                                    html.H6("Level over time", className="mb-2"),
                                    dcc.Graph(id="china_line")
                                ], className="col-12 col-lg-7"),
                                html.Div([
                                    html.H6("YoY growth (%)", className="mb-2"),
                                    dcc.Graph(id="china_yoy")
                                ], className="col-12 col-lg-5"),
                            ], className="row g-3"),

                            html.Div([
                                html.I(className="bi bi-info-circle me-2 text-primary"),
                                html.Small("YoY = (current − previous) / previous × 100%. 'GDP' here equals Population × GDP per Capita.")
                            ], className="text-muted mt-2")
                        ], className="card-body pt-2"),
                    ], className="card shadow-sm")
                ], className="mb-4")
            ]
        ),
    ])
], className="col-10 col-lg-8 mx-auto", style={"backgroundColor": "#e5ecf6", "minHeight": "100vh", "paddingBottom": "12px"})

##################### CALLBACKS ################################
@callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value")])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value")])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value")])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value")])
def update_map(var_map_value, year):
    return create_choropleth_map(var_map_value, year)

# 中国趋势：返回折线与同比两个图
@callback(
    [Output("china_line", "figure"), Output("china_yoy", "figure")],
    [Input("china_var", "value")]
)
def update_china_trends(indicator):
    china_df = gapminder_df[gapminder_df["Country"] == "China"].sort_values("Year").copy()
    # 折线：数值随年份变化
    line_fig = px.line(
        china_df,
        x="Year",
        y=indicator,
        markers=True,
        title=f"China {indicator} over time"
    )
    line_fig.update_layout(paper_bgcolor="#e5ecf6", height=420, margin={"l":40, "r":10, "t":50, "b":30})

    # 同比：百分比
    china_df["YoY"] = china_df[indicator].pct_change() * 100.0
    yoy_fig = px.bar(
        china_df,
        x="Year",
        y="YoY",
        title=f"China {indicator} YoY growth (%)",
        color="YoY",
        color_continuous_scale="RdYlGn"
    )
    yoy_fig.update_layout(paper_bgcolor="#e5ecf6", height=420, margin={"l":40, "r":10, "t":50, "b":30}, showlegend=False)
    return line_fig, yoy_fig

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8050)