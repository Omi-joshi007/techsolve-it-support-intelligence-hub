from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from agent.support_agent import ask_support_agent_async

BASE = Path(__file__).resolve().parent
STATIC = BASE / "static"
app = FastAPI(title="TechSolve Support Intelligence Agent")
app.mount("/static", StaticFiles(directory=STATIC), name="static")

class QuestionRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)

@app.get("/")
async def home():
    return FileResponse(STATIC / "index.html")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/ask")
async def ask(payload: QuestionRequest):
    try:
        return {"answer": await ask_support_agent_async(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="The agent could not complete the analysis.") from exc
