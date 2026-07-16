# TechSolve IT Support Intelligence Hub

This is the simple starter code for Part 1 of the practical assessment:

> Source, Combine & Prepare

The project:

1. reads the supplied Excel ticket data;
2. cleans and validates the ticket records;
3. standardises issue categories and subcategories;
4. adds New Zealand public holiday information;
5. adds historical New Zealand weather information;
6. exports cleaned files for the dashboard and AI agent.

## Project structure

```text
techsolve-it-support-intelligence-hub/
├── data/
│   ├── raw/
│   │   └── TechSolve - Ticket Data.xlsx
│   ├── external/
│   │   ├── nz_public_holidays.csv
│   │   └── nz_weather.csv
│   └── processed/
│       ├── cleaned_enriched_ticket_data.csv
│       └── tickets_2024_2025.csv
│
├── clean_data.py
├── add_external_data.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## What each file does

### clean_data.py

- reads and cleans ticket values;
- fixes column names;
- removes exact duplicate rows;
- converts date and numeric columns;
- standardises categories and subcategories;
- flags invalid dates and questionable records;
- creates reporting columns.

### add_external_data.py

- creates NZ public holiday data;
- downloads historical weather from Open-Meteo;
- combines both sources with ticket data.

### main.py

Runs all steps in the correct order and saves the final output files.

## Setup in VS Code on Mac

### 1. Place the raw Excel file

Copy the supplied Excel file to:

```text
data/raw/TechSolve - Ticket Data.xlsx
```

### 2. Create a virtual environment

Open the VS Code terminal and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Run the project

```bash
python main.py
```

The weather download requires an internet connection.

## Output files

### Full cleaned and enriched data

```text
data/processed/cleaned_enriched_ticket_data.csv
```

This keeps all valid and questionable rows for transparency.

### Requested 2024-2025 reporting data

```text
data/processed/tickets_2024_2025.csv
```

Use this file for the dashboard because the brief requests 2024-2025 reporting.

## Important notes

- The original Excel workbook is never overwritten.
- Invalid-looking dates are flagged rather than silently deleted.
- Original issue categories are retained in `category_original`.
- Weather uses one representative city for each region and should be described as a regional proxy.
- Public holiday and weather patterns show association, not definite causation.
- Do not expose customer email addresses in a public dashboard.
