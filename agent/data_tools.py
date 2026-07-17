from pathlib import Path
import json

import pandas as pd

from agents import function_tool


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "tickets_2024_2025.csv"
)


def load_ticket_data() -> pd.DataFrame:
    """Load and prepare the final ticket dataset."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Ticket dataset was not found at: {DATA_FILE}"
        )

    df = pd.read_csv(
        DATA_FILE,
        low_memory=False,
    )

    # Convert date columns.
    date_columns = [
        "ticket_created_date_clean",
        "ticket_resolved_date_clean",
        "ticket_date",
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    # Convert numeric columns.
    numeric_columns = [
        "resolution_time_hours",
        "first_response_time_hours",
        "sla_target_hours",
        "csat_score",
        "issue_complexity_score",
        "previous_tickets",
        "monthly_contract_value",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    # Convert Boolean-like text columns.
    boolean_columns = [
        "calculated_sla_breach",
        "sla_breached",
        "sla_breach_mismatch",
        "is_open_ticket",
        "is_unassigned",
        "escalated",
        "is_public_holiday",
        "is_business_day",
        "is_weekend",
    ]

    true_values = {
        "true",
        "yes",
        "1",
        "y",
    }

    false_values = {
        "false",
        "no",
        "0",
        "n",
    }

    for column in boolean_columns:
        if column in df.columns:
            normalised = (
                df[column]
                .astype("string")
                .str.strip()
                .str.lower()
            )

            df[column] = normalised.map(
                lambda value: (
                    True
                    if value in true_values
                    else False
                    if value in false_values
                    else pd.NA
                )
            ).astype("boolean")

    return df


# Load the dataset only once when the application starts.
tickets_df = load_ticket_data()


def make_json_serialisable(value):
    """Convert Pandas and NumPy values into JSON-safe values."""

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    return value


def records_to_json(records: list[dict]) -> str:
    """Convert analytical records into formatted JSON."""

    cleaned_records = []

    for record in records:
        cleaned_record = {
            key: make_json_serialisable(value)
            for key, value in record.items()
        }

        cleaned_records.append(cleaned_record)

    return json.dumps(
        cleaned_records,
        indent=2,
    )


# Tool 1: Dataset overview

@function_tool
def get_dataset_overview() -> str:
    """
    Return a high-level overview of the support ticket dataset.

    Use this tool for questions about dataset size, date coverage,
    total tickets, open tickets, escalations, SLA breaches and CSAT.
    """

    df = tickets_df

    total_tickets = len(df)

    start_date = None
    end_date = None

    if "ticket_date" in df.columns:
        start_date = df["ticket_date"].min()
        end_date = df["ticket_date"].max()

    overview = {
        "total_tickets": total_tickets,
        "date_start": (
            start_date.strftime("%Y-%m-%d")
            if pd.notna(start_date)
            else None
        ),
        "date_end": (
            end_date.strftime("%Y-%m-%d")
            if pd.notna(end_date)
            else None
        ),
        "open_tickets": (
            int(
                df["is_open_ticket"]
                .fillna(False)
                .astype(bool)
                .sum()
            )
            if "is_open_ticket" in df.columns
            else None
        ),
        "escalated_tickets": (
            int(
                df["escalated"]
                .fillna(False)
                .astype(bool)
                .sum()
            )
            if "escalated" in df.columns
            else None
        ),
        "calculated_sla_breaches": (
            int(
                df["calculated_sla_breach"]
                .fillna(False)
                .astype(bool)
                .sum()
            )
            if "calculated_sla_breach" in df.columns
            else None
        ),
        "average_resolution_hours": (
            round(
                df["resolution_time_hours"]
                .dropna()
                .mean(),
                2,
            )
            if "resolution_time_hours" in df.columns
            else None
        ),
        "average_csat": (
            round(
                df["csat_score"]
                .dropna()
                .mean(),
                2,
            )
            if "csat_score" in df.columns
            else None
        ),
    }

    return json.dumps(
        overview,
        indent=2,
    )

# Tool 2: Ticket trends

@function_tool
def get_monthly_ticket_trends(year: int = 2024) -> str:
    """
    Calculate monthly ticket volume for a selected year.

    Use this tool for questions about monthly ticket trends,
    increasing or decreasing ticket volume and peak periods.

    Args:
        year: Reporting year to analyse, such as 2024 or 2025.
    """

    df = tickets_df.copy()

    if "ticket_date" not in df.columns:
        return json.dumps(
            {"error": "ticket_date column is unavailable"}
        )

    filtered = df[
        df["ticket_date"].dt.year == year
    ].copy()

    if filtered.empty:
        return json.dumps(
            {
                "year": year,
                "message": "No tickets found for this year.",
            }
        )

    monthly = (
        filtered
        .groupby(
            filtered["ticket_date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="ticket_count")
    )

    monthly["month"] = (
        monthly["ticket_date"]
        .astype(str)
    )

    monthly = monthly[
        ["month", "ticket_count"]
    ]

    return records_to_json(
        monthly.to_dict(orient="records")
    )

# Tool 3: Team performance

@function_tool
def get_team_performance(top_n: int = 10) -> str:
    """
    Compare support teams by ticket volume, SLA breach rate,
    average resolution time and average CSAT.

    Use this tool for questions about team performance,
    overloaded teams or teams requiring management attention.

    Args:
        top_n: Maximum number of teams to return.
    """

    df = tickets_df.copy()

    if "team" not in df.columns:
        return json.dumps(
            {"error": "team column is unavailable"}
        )

    summary = (
        df.groupby(
            "team",
            dropna=False,
        )
        .agg(
            ticket_count=(
                "ticket_id",
                "count",
            ),
            average_resolution_hours=(
                "resolution_time_hours",
                "mean",
            ),
            average_csat=(
                "csat_score",
                "mean",
            ),
        )
        .reset_index()
    )

    if "calculated_sla_breach" in df.columns:
        breach_summary = (
        df.groupby(
            "team",
            dropna=False,
        )["calculated_sla_breach"]
        .apply(
            lambda values: (
                values.dropna().mean() * 100
                if not values.dropna().empty
                else None
            )
        )
        .reset_index(
            name="sla_breach_rate_percent"
        )
    )

    summary = summary.merge(
        breach_summary,
        on="team",
        how="left",
    )

    summary["average_resolution_hours"] = (
        summary["average_resolution_hours"]
        .round(2)
    )

    summary["average_csat"] = (
        summary["average_csat"]
        .round(2)
    )

    if "sla_breach_rate_percent" in summary.columns:
        summary["sla_breach_rate_percent"] = (
            summary["sla_breach_rate_percent"]
            .round(2)
        )

    summary = (
        summary
        .sort_values(
            "ticket_count",
            ascending=False,
        )
        .head(max(1, min(top_n, 20)))
    )

    return records_to_json(
        summary.to_dict(orient="records")
    )

# Tool 4: Common problem areas

@function_tool
def get_problem_areas(
    dimension: str = "standard_category",
    top_n: int = 10,
) -> str:
    """
    Identify the most common ticket problem areas.

    Use this tool to analyse categories, subcategories, regions,
    industries, customer segments, operating systems or browsers.

    Args:
        dimension: Column to analyse. Supported values are
            standard_category, standard_subcategory, region,
            industry, customer_segment, operating_system and browser.
        top_n: Maximum number of results to return.
    """

    allowed_dimensions = {
        "standard_category",
        "standard_subcategory",
        "region",
        "industry",
        "customer_segment",
        "operating_system",
        "browser",
    }

    if dimension not in allowed_dimensions:
        return json.dumps(
            {
                "error": "Unsupported dimension.",
                "allowed_dimensions": sorted(
                    allowed_dimensions
                ),
            },
            indent=2,
        )

    if dimension not in tickets_df.columns:
        return json.dumps(
            {
                "error": (
                    f"{dimension} is not available "
                    "in the dataset."
                )
            }
        )

    result = (
        tickets_df[dimension]
        .fillna("Unknown")
        .value_counts()
        .head(max(1, min(top_n, 20)))
        .rename_axis(dimension)
        .reset_index(name="ticket_count")
    )

    result["percentage_of_tickets"] = (
        result["ticket_count"]
        .div(len(tickets_df))
        .mul(100)
        .round(2)
    )

    return records_to_json(
        result.to_dict(orient="records")
    )

# Tool 5: Filtered operational analysis

@function_tool
def analyse_ticket_segment(
    region: str = "",
    team: str = "",
    category: str = "",
    year: int = 0,
) -> str:
    """
    Analyse a filtered segment of ticket data.

    Use this tool when a question specifies a region, team,
    standard ticket category or reporting year.

    Leave a parameter empty or zero when it is not requested.

    Args:
        region: Region name, for example Canterbury.
        team: Support team name.
        category: Standard ticket category.
        year: Reporting year, such as 2024.
    """

    df = tickets_df.copy()

    applied_filters = {}

    if region:
        df = df[
            df["region"]
            .fillna("")
            .str.casefold()
            == region.casefold()
        ]

        applied_filters["region"] = region

    if team:
        df = df[
            df["team"]
            .fillna("")
            .str.casefold()
            == team.casefold()
        ]

        applied_filters["team"] = team

    if category:
        df = df[
            df["standard_category"]
            .fillna("")
            .str.casefold()
            == category.casefold()
        ]

        applied_filters["category"] = category

    if year:
        df = df[
            df["ticket_date"].dt.year == year
        ]

        applied_filters["year"] = year

    if df.empty:
        return json.dumps(
            {
                "applied_filters": applied_filters,
                "ticket_count": 0,
                "message": (
                    "No matching ticket records were found."
                ),
            },
            indent=2,
        )

    result = {
        "applied_filters": applied_filters,
        "ticket_count": len(df),
        "percentage_of_all_tickets": round(
            len(df) / len(tickets_df) * 100,
            2,
        ),
        "average_resolution_hours": round(
            df["resolution_time_hours"]
            .dropna()
            .mean(),
            2,
        ),
        "average_first_response_hours": round(
            df["first_response_time_hours"]
            .dropna()
            .mean(),
            2,
        ),
        "average_csat": round(
            df["csat_score"]
            .dropna()
            .mean(),
            2,
        ),
        "sla_breach_rate_percent": round(
            df["calculated_sla_breach"]
            .fillna(False)
            .mean()
            * 100,
            2,
        ),
        "escalation_rate_percent": round(
            df["escalated"]
            .astype(str)
            .str.lower()
            .isin(["true", "yes", "1"])
            .mean()
            * 100,
            2,
        ),
    }

    return json.dumps(
        result,
        indent=2,
    )

