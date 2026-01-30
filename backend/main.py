from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks
from routers.chat import router as chat_router
from database import create_db_and_tables
from src.api.v1.recurring_tasks import router as recurring_tasks_router
from src.api.v1.reminders import router as reminders_router
from src.api.v1.events import router as events_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

# FIXED: Add prefix here!
app.include_router(chat_router, tags=["chat"])

# Include new Phase 5 endpoints
app.include_router(recurring_tasks_router, prefix="/api/v1/recurring-tasks", tags=["recurring-tasks"])
app.include_router(reminders_router, prefix="/api/v1/reminders", tags=["reminders"])
app.include_router(events_router, prefix="/api/v1/events", tags=["events"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # ← note: you said 8001 earlier, decide one