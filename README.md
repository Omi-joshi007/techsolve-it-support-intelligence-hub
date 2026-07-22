# TechSolve IT

TechSolve IT is an AI-powered support operations project that transforms synthetic IT support ticket data into interactive dashboards, operational insights and natural-language answers.

The project combines Python-based data preparation, a five-page Power BI dashboard and an AI support analytics agent.

## Live Applications

### Power BI Dashboard

[Open the Live Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYjM3MTJmMDItOTYyNy00ZTIyLTgzNjktZTA0NWFhY2FmMjgzIiwidCI6IjY0NzEyM2UzLTY0Y2UtNDE0Yi1iOTU5LTQ4ZDEwZDExNTMyNCJ9&pageName=671004460a2c8da2b0b0)

### AI Support Agent

[Open the Live AI Agent](https://techsolve-it-ai-agent.onrender.com/)

> The AI Agent is hosted on Render’s free tier. It may take approximately one minute to restart after a period of inactivity.

---

## Power BI Dashboard

The Power BI report contains five pages:

1. **Executive Overview**  
   Overall ticket volume, backlog, SLA compliance, response time, resolution time, escalation rate and CSAT.

2. **Issue Analysis**  
   Ticket categories, subcategories, recurring issues, priority mix, resolution time and SLA breach rates.

3. **Resolution and SLA Performance**  
   Response efficiency, resolution performance, SLA breaches, escalation rates and open-ticket ageing.

4. **Team Performance**  
   Team workload, backlog, SLA compliance, resolution time, escalation rate, CSAT and analyst workload with priority and complexity context.

5. **Holiday and Operational Impact**  
   Ticket volume, SLA performance, resolution time and backlog patterns around New Zealand public holidays, weekdays and weekends.

### Dashboard Preview

<img width="1482" height="827" alt="image" src="https://github.com/user-attachments/assets/f4669453-30f1-4224-99a8-2763a3264891" />


---

## AI Support Agent

The AI Agent allows users to ask natural-language questions about:

- Ticket trends
- Team workload and performance
- SLA breaches
- Response and resolution times
- Issue categories and recurring problems
- Customer and regional trends
- Operational areas requiring attention

Pandas performs the calculations, while the OpenAI model interprets the question and explains the results.

### AI Agent Preview

<img width="767" height="742" alt="image" src="https://github.com/user-attachments/assets/f255dc22-f5aa-4b5e-b82d-9b1cdc791899" />


---

## Data Preparation

The data preparation workflow was completed using Python and Jupyter Notebook.

Key steps included:

- Inspecting and validating the supplied ticket dataset
- Cleaning missing, duplicate and inconsistent records
- Standardising ticket categories and subcategories
- Validating ticket dates, SLA results and resolution metrics
- Creating reporting and operational fields
- Adding New Zealand public holiday information
- Exporting a final analysis-ready dataset

Final processed dataset:

```text
data/processed/tickets_2024_2025.csv
