from dash import Dash, html, dcc, Input, Output
import webbrowser
import pandas as pd
import plotly.express as px


app = Dash(__name__)

amazon_df = pd.read_csv("amazon_sales.csv")
student_df = pd.read_csv("StudentsPerformance.csv.csv")


total_orders = len(amazon_df)

total_revenue = round(
    amazon_df["TotalAmount"].sum(),
    2
)

total_students = len(student_df)

avg_math_score = round(
    student_df["math score"].mean(),
    2
)
category_revenue = (
    amazon_df.groupby("Category")["TotalAmount"]
    .sum()
    .reset_index()
)

country_revenue = (
    amazon_df.groupby("Country")["TotalAmount"]
    .sum()
    .reset_index()
)

amazon_bar = px.bar(
    category_revenue,
    x="Category",
    y="TotalAmount",
    title="Revenue by Category"
)

amazon_pie = px.pie(
    country_revenue,
    names="Country",
    values="TotalAmount",
    title="Revenue by Country"
)

student_gender = px.pie(
    student_df,
    names="gender",
    title="Gender Distribution"
)

student_math = px.histogram(
    student_df,
    x="math score",
    title="Math Score Distribution"
)


student_reading = px.histogram(
    student_df,
    x="reading score",
    title="Reading Score Distribution"
)

student_writing = px.histogram(
    student_df,
    x="writing score",
    title="Writing Score Distribution"
)


top_products = (
    amazon_df.groupby("ProductName")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

product_chart = px.bar(
    top_products,
    x="ProductName",
    y="TotalAmount",
    title="Top 10 Products"
)

top_countries = (
    amazon_df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

country_chart = px.bar(
    top_countries,
    x="Country",
    y="TotalAmount",
    title="Country Revenue Analysis"
)

sidebar = html.Div(

    children=[

        html.H2(
            "📊 MENU",
            style={
                "textAlign": "center",
                "color": "white",
                "marginBottom": "30px"
            }
        ),

        html.Hr(style={"border": "1px solid white"}),

        dcc.RadioItems(
            id="menu",
            options=[
                {"label": "🏠 Home", "value": "home"},
                {"label": "📊 Amazon Analytics", "value": "amazon"},
                {"label": "🎓 Student Analytics", "value": "student"},
                {"label": "🤖 ML Prediction", "value": "prediction"},
                {"label": "ℹ About Project", "value": "about"},
            ],

            value="home",

            labelStyle={
                "display": "block",
                "marginBottom": "20px",
                "fontSize": "20px",
                "color": "white",
                "fontWeight": "bold",
                "cursor": "pointer"
            },

            inputStyle={
                "marginRight": "10px"
            }

        )

    ],

    style={
        "width": "20%",
        "height": "100vh",
        "background": "linear-gradient(to bottom, #0F172A, #1E293B)",
        "color": "white",
        "padding": "25px",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "boxShadow": "3px 0px 15px rgba(0,0,0,0.5)"
    }
)

content = html.Div(

    id="page-content",

    style={
        "marginLeft": "22%",
        "padding": "30px",
        "fontFamily": "Arial"
    }

)

app.layout = html.Div([
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    Input("menu", "value")
)
def update_page(page):

    if page == "home":

        return [

        html.H1("CODTECH Integrated Analytics Dashboard"),
        html.Hr(),
        html.H2("Dashboard Overview"),
        html.Br(),

        html.Div([

            html.Div([
                html.H3("💰 Total Revenue"),
                html.H1(f"₹ {total_revenue}")
            ], style={
                "backgroundColor":"#2563EB",
                "color":"white",
                "padding":"25px",
                "borderRadius":"15px",
                "width":"250px",
                "textAlign":"center"
            }),

            html.Div([
                html.H3("📦 Total Orders"),
                html.H1(f"{total_orders}")
            ], style={
                "backgroundColor":"#059669",
                "color":"white",
                "padding":"25px",
                "borderRadius":"15px",
                "width":"250px",
                "textAlign":"center"
            }),

            html.Div([
                html.H3("🎓 Students"),
                html.H1(f"{total_students}")
            ], style={
                "backgroundColor":"#DC2626",
                "color":"white",
                "padding":"25px",
                "borderRadius":"15px",
                "width":"250px",
                "textAlign":"center"
            }),

            html.Div([
                html.H3("📊 Avg Math Score"),
                html.H1(f"{avg_math_score}")
            ], style={
                "backgroundColor":"#7C3AED",
                "color":"white",
                "padding":"25px",
                "borderRadius":"15px",
                "width":"250px",
                "textAlign":"center"
            })

        ], style={
            "display":"flex",
            "gap":"20px",
            "flexWrap":"wrap"
        })
    ]

    elif page == "amazon":

         return [

        html.H1("📊 Amazon Analytics Dashboard"),
        html.Hr(),

        html.H3("Revenue By Category"),
        dcc.Graph(figure=amazon_bar),

        html.H3("Revenue By Country"),
        dcc.Graph(figure=amazon_pie),

        html.H3("Top 10 Products"),
        dcc.Graph(figure=product_chart),

        html.H3("Country Revenue Analysis"),
        dcc.Graph(figure=country_chart)

    ]

    elif page == "student":
      return [

    html.H1("🎓 Student Analytics Dashboard"),
    html.Hr(),

    html.H3("Gender Distribution"),
    dcc.Graph(figure=student_gender),

    html.H3("Math Score Distribution"),
    dcc.Graph(figure=student_math),

    html.H3("Reading Score Distribution"),
    dcc.Graph(figure=student_reading),

    html.H3("Writing Score Distribution"),
    dcc.Graph(figure=student_writing)

]

    elif page == "prediction":
      return [

    html.H1("🤖 Machine Learning Prediction"),
    html.Hr(),

    html.Div([

        html.H3("Student Performance Predictor"),

        html.Br(),

        html.Label("Reading Score"),
        dcc.Input(
            id="reading",
            type="number",
            value=50,
            style={"width":"300px"}
        ),

        html.Br(),
        html.Br(),

        html.Label("Writing Score"),
        dcc.Input(
            id="writing",
            type="number",
            value=50,
            style={"width":"300px"}
        ),

        html.Br(),
        html.Br(),

        html.Button(
            "Predict Math Score",
            id="predict-btn",
            n_clicks=0,
            style={
                "backgroundColor":"#2563EB",
                "color":"white",
                "padding":"12px",
                "border":"none",
                "borderRadius":"10px"
            }
        ),

        html.Br(),
        html.Br(),

        html.Div(
            id="prediction-output",
            style={
                "fontSize":"25px",
                "fontWeight":"bold",
                "color":"green"
            }
        )

    ])

]

    elif page == "about":
     return [

    html.H1("ℹ About Project"),
    html.Hr(),

    html.H3("Task 1"),
    html.P("Big Data Analysis using Dask"),

    html.H3("Task 2"),
    html.P("Predictive Analysis using Machine Learning"),

    html.H3("Task 3"),
    html.P("Interactive Dashboard Development using Dash")

]
@app.callback(
    Output("prediction-output", "children"),
    Input("predict-btn", "n_clicks"),
    Input("reading", "value"),
    Input("writing", "value")
)
def predict_score(n_clicks, reading, writing):

    if n_clicks == 0:
        return ""

    prediction = round(
        (reading + writing) / 2,
        2
    )

    return f"Predicted Math Score: {prediction}"
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/")
    app.run(debug=True)