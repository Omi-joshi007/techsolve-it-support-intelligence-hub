# TechSolve IT Support Intelligence Hub

An end-to-end support analytics project designed to improve visibility into ticket issues, resolution performance, SLA compliance and operational improvement opportunities.

## Current Progress

### Part 1 — Data Preparation

Completed using Python and Jupyter Notebook:

* Inspected dataset structure, data types and missing values
* Removed exact duplicate records
* Standardised ticket categories and subcategories
* Flagged invalid dates and inconsistent SLA values
* Created reporting-ready date and performance fields
* Added New Zealand public holiday data
* Exported cleaned datasets for dashboard development

## Project Structure

```text
├── data/
│   ├── raw/
│   ├── external/
│   └── processed/
├── notebooks/
│   └── data_preparation.ipynb
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open `data_preparation.ipynb` in VS Code and run the cells from top to bottom.

## Next Steps

* Build the interactive support analytics dashboard
* Develop the AI-powered operations assistant
* Deploy the completed solution online

> The dataset used in this project is entirely synthetic.
