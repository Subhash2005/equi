from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_indexes
from seed import seed
import auth, student, daily_worker, investment, disability, ledger

app = FastAPI(title="EquiBridge API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for deployment, refine later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_indexes()
    seed()


@app.get("/")
def root():
    return {"message": "Welcome to EquiBridge API ", "docs": "/docs", "version": "2.0.0", "db": "MongoDB"}


app.include_router(auth.router)
app.include_router(student.router)
app.include_router(daily_worker.router)
app.include_router(investment.router)
app.include_router(disability.router)
app.include_router(ledger.router)
