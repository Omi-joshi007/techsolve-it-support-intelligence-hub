from dash import ALL, Dash, Input, Output, State, callback, ctx, dcc, html
from agent.support_agent import ask_support_agent

app = Dash(__name__, assets_folder="assets")
server = app.server
app.title = "TechSolve AI Support Intelligence"

EXAMPLES = [
    "Which teams require management attention?",
    "What are the most common ticket categories?",
    "How did monthly ticket volume change in 2024?",
    "How is the Canterbury region performing?",
]

app.layout = html.Div(className="page", children=[
    html.Div(className="orb orb-one"),
    html.Div(className="orb orb-two"),
    html.Header(className="hero", children=[
        html.Div(className="brand", children=[
            html.Div("TS", className="logo"),
            html.Div([html.P("TECHSOLVE", className="eyebrow"), html.H1("Support Intelligence Agent")]),
        ]),
        html.P("Ask operational questions and receive evidence-backed insights calculated directly from the prepared ticket dataset.", className="subtitle"),
        html.Div(className="badges", children=[
            html.Span("● Agent online", className="badge online"),
            html.Span("Pandas grounded", className="badge"),
            html.Span("OpenAI powered", className="badge"),
        ]),
    ]),
    html.Main(className="grid", children=[
        html.Section(className="card", children=[
            html.P("OPERATIONS COPILOT", className="eyebrow"),
            html.H2("What would you like to know?"),
            dcc.Textarea(id="question", className="question", placeholder="Which team has the highest SLA breach rate?"),
            html.Div(className="actions", children=[
                html.Button("✦ Ask the agent", id="ask", className="primary"),
                html.Button("Clear", id="clear", className="secondary"),
            ]),
            html.P("TRY A QUESTION", className="eyebrow examples-title"),
            html.Div(className="chips", children=[
                html.Button(q, id={"type": "example", "index": i}, className="chip") for i, q in enumerate(EXAMPLES)
            ]),
        ]),
        html.Section(className="card", children=[
            html.Div(className="answer-head", children=[
                html.Div([html.P("AGENT RESPONSE", className="eyebrow"), html.H2("Operational insight")]),
                html.Div("AI", className="ai"),
            ]),
            dcc.Loading(type="circle", children=html.Div(id="answer", className="answer empty", children=[
                html.Div("✦", className="spark"),
                html.H3("Your evidence-backed answer will appear here"),
                html.P("The agent selects a controlled analytical tool, calculates with Pandas, and explains the result."),
            ])),
        ]),
    ]),
    html.Footer("Synthetic assessment dataset • Calculations performed locally with Pandas")
])

@callback(Output("question", "value"), Input({"type": "example", "index": ALL}, "n_clicks"), Input("clear", "n_clicks"), State("question", "value"), prevent_initial_call=True)
def set_question(_, __, current):
    if ctx.triggered_id == "clear":
        return ""
    if isinstance(ctx.triggered_id, dict):
        return EXAMPLES[ctx.triggered_id["index"]]
    return current

@callback(Output("answer", "children"), Output("answer", "className"), Input("ask", "n_clicks"), State("question", "value"), prevent_initial_call=True)
def run_agent(_, question):
    if not question or not question.strip():
        return "Please enter a question first.", "answer error"
    try:
        return dcc.Markdown(ask_support_agent(question)), "answer populated"
    except Exception as exc:
        return f"Agent error: {exc}", "answer error"

if __name__ == "__main__":
    app.run(debug=True)
