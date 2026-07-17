# TechSolve IT

TechSolve IT, AI-powered support operations platform that analyses IT support ticket data and provides evidence-based operational insights through natural-language questions.

## Current Progress

### Part 1 — Data Preparation

Completed using Python and Jupyter Notebook:

* Inspected the source ticket dataset
* Cleaned missing, duplicate and inconsistent records
* Standardised ticket categories and subcategories
* Created reporting and SLA validation fields
* Added New Zealand public holiday data
* Exported a final analysis-ready dataset

Final dataset:

```text
data/processed/tickets_2024_2025.csv
```

### Part 3 — AI Agent

Completed using:

* Python
* Pandas
* OpenAI Agents SDK
* FastAPI
* HTML, CSS and JavaScript

The AI agent can answer operational questions about:

* ticket trends
* team performance
* SLA breaches
* resolution times
* ticket categories
* customer and regional problem areas

Pandas performs the calculations, while the OpenAI model interprets questions and explains the results.

## Project Structure

```text
├── agent/
│   ├── __init__.py
│   ├── data_tools.py
│   └── support_agent.py
├── custom_app/
│   ├── __init__.py
│   ├── api.py
│   └── static/
│       ├── index.html
│       ├── styles.css
│       ├── app.js
│       └── favicon.svg
├── data/
│   ├── raw/
│   ├── external/
│   └── processed/
│       └── tickets_2024_2025.csv
├── notebook/
│   └── data_preparation.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_openai_api_key
```

Run the application:

```bash
uvicorn custom_app.api:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Security

The OpenAI API key is stored in environment variables and is not committed to GitHub.

The agent uses predefined Pandas tools and does not allow unrestricted Python execution.

## Data Limitation

The dataset contains very limited records for 2025. The agent therefore avoids making strong year-over-year conclusions without clearly identifying this limitation.

## Next Step

Build the Power BI dashboard using the same final processed dataset.

> The dataset used in this project is entirely synthetic.
