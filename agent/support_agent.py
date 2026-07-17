from dotenv import load_dotenv
from agents import Agent, Runner

from agent.data_tools import (
    analyse_ticket_segment,
    get_dataset_overview,
    get_monthly_ticket_trends,
    get_problem_areas,
    get_team_performance,
)

load_dotenv()

support_agent = Agent(
    name="TechSolve Support Intelligence Agent",
    instructions="""
You are an operational support-data analyst for TechSolve.
Always use the available tools for dataset questions.
Never invent counts, percentages, averages, trends, or rankings.
Pandas tool outputs are the source of truth.
Answer with: direct answer, evidence, recommendation, and limitations when relevant.
Keep responses concise and management-friendly.
The dataset has very limited 2025 coverage, so avoid strong year-over-year conclusions.
""",
    tools=[
        get_dataset_overview,
        get_monthly_ticket_trends,
        get_team_performance,
        get_problem_areas,
        analyse_ticket_segment,
    ],
)

def ask_support_agent(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a question about the support dataset."
    result = Runner.run_sync(support_agent, question)
    return str(result.final_output)

async def ask_support_agent_async(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a question about the support dataset."
    result = await Runner.run(support_agent, question)
    return str(result.final_output)
