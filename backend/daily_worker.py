from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
from database import daily_workers_col, work_listings_col, ledger_col

router = APIRouter(prefix="/daily", tags=["daily"])


class WorkerRegisterRequest(BaseModel):
    user_email: str
    name: str
    location: str
    problem_type: str = ""
    photo_url: str = ""


class WorkRequest(BaseModel):
    user_email: str
    location: str
    problem_type: str
    photo_url: str
    description: Optional[str] = ""


class AcceptJobRequest(BaseModel):
    user_email: str
    job_id: str


class CompleteJobRequest(BaseModel):
    user_email: str
    job_id: str
    completion_video_url: str = ""
    ai_verified: bool = False


class WithdrawRequest(BaseModel):
    user_email: str
    amount: float


class ToggleInvestRequest(BaseModel):
    user_email: str


@router.post("/post-problem")
def post_problem(req: WorkRequest):
    doc = {
        "user_email": req.user_email,
        "location": req.location,
        "problem_type": req.problem_type,
        "photo_url": req.photo_url,  # This is the "proof pic" of the problem
        "description": req.description,
        "status": "open",
        "created_at": datetime.utcnow()
    }
    result = work_listings_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


def _sid(doc):
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/register")
def register_worker(req: WorkerRegisterRequest):
    existing = daily_workers_col.find_one({"user_email": req.user_email})
    if existing:
        # Update location and problem type on re-login
        daily_workers_col.update_one(
            {"user_email": req.user_email},
            {"$set": {
                "location": req.location,
                "problem_type": req.problem_type,
                "photo_url": req.photo_url,
                "last_seen": datetime.utcnow(),
            }}
        )
        updated = daily_workers_col.find_one({"user_email": req.user_email})
        return _sid(updated)

    doc = {
        "user_email": req.user_email,
        "name": req.name,
        "location": req.location,
        "problem_type": req.problem_type,
        "photo_url": req.photo_url,
        "balance": 0.0,
        "total_earned": 0.0,
        "invested_amount": 0.0,
        "auto_invest": False,
        "created_at": datetime.utcnow(),
        "last_seen": datetime.utcnow(),
    }
    result = daily_workers_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


@router.get("/me/{user_email}")
def get_worker(user_email: str):
    worker = daily_workers_col.find_one({"user_email": user_email})
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return _sid(worker)


@router.get("/nearby")
def get_nearby_workers(location: str = "", problem_type: str = "", limit: int = 10):
    """Return workers near a location who match a problem type."""
    query = {}
    if problem_type:
        query["problem_type"] = problem_type
    if location:
        # Simple substring match for city/area name
        query["location"] = {"$regex": location.split(",")[0].strip(), "$options": "i"}

    workers = list(daily_workers_col.find(query).limit(limit))
    for w in workers:
        w["id"] = str(w.pop("_id"))
        # Remove sensitive info
        w.pop("balance", None)
        w.pop("total_earned", None)
    return workers


@router.get("/work")
def get_work():
    jobs = list(work_listings_col.find({"status": "open"}))
    for j in jobs:
        j["id"] = str(j.pop("_id"))
    return jobs


@router.post("/accept")
def accept_job(req: AcceptJobRequest):
    job = work_listings_col.find_one({"_id": ObjectId(req.job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    work_listings_col.update_one(
        {"_id": ObjectId(req.job_id)},
        {"$set": {"status": "in_progress", "accepted_by": req.user_email}}
    )
    return {"message": f"Job '{job['title']}' accepted!", "pay": job["pay"]}


@router.post("/complete")
def complete_job(req: CompleteJobRequest):
    job = work_listings_col.find_one({"_id": ObjectId(req.job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    pay = job["pay"]
    work_listings_col.update_one(
        {"_id": ObjectId(req.job_id)},
        {"$set": {
            "status": "completed",
            "completion_video_url": req.completion_video_url,
            "ai_verified": req.ai_verified,
        }}
    )
    daily_workers_col.update_one(
        {"user_email": req.user_email},
        {"$inc": {"balance": pay, "total_earned": pay}}
    )
    ledger_col.insert_one({
        "user_email": req.user_email,
        "type": "credit",
        "amount": pay,
        "description": f"Completed: {job['title']}" + (" (AI Verified ✅)" if req.ai_verified else ""),
        "timestamp": datetime.utcnow(),
    })
    worker = daily_workers_col.find_one({"user_email": req.user_email})
    return {"message": "Job completed!", "pay": pay, "new_balance": worker["balance"]}


@router.get("/revenue/{user_email}")
def get_revenue(user_email: str):
    worker = daily_workers_col.find_one({"user_email": user_email})
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return _sid(worker)


@router.post("/toggle-invest")
def toggle_invest(req: ToggleInvestRequest):
    worker = daily_workers_col.find_one({"user_email": req.user_email})
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    new_val = not worker.get("auto_invest", False)
    daily_workers_col.update_one({"user_email": req.user_email}, {"$set": {"auto_invest": new_val}})
    return {"auto_invest": new_val, "message": f"Auto-invest {'enabled' if new_val else 'disabled'}"}


@router.post("/withdraw")
def withdraw(req: WithdrawRequest):
    worker = daily_workers_col.find_one({"user_email": req.user_email})
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    if worker["balance"] < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    daily_workers_col.update_one({"user_email": req.user_email}, {"$inc": {"balance": -req.amount}})
    ledger_col.insert_one({
        "user_email": req.user_email,
        "type": "debit",
        "amount": req.amount,
        "description": "Withdrawal to bank account",
        "timestamp": datetime.utcnow(),
    })
    worker = daily_workers_col.find_one({"user_email": req.user_email})
    return {"message": "Withdrawal successful", "withdrawn": req.amount, "new_balance": worker["balance"]}
