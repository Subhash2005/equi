from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from database import disability_users_col, disability_jobs_col, ledger_col

router = APIRouter(prefix="/disability", tags=["disability"])


class DisabilityRegisterRequest(BaseModel):
    user_email: str
    name: str
    id_proof: str
    profession: str
    disability_type: str
    skills: List[str] = []


class PostJobRequest(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str]
    pay: float
    profession: str = ""


class AcceptJobRequest(BaseModel):
    user_email: str
    job_id: str


class StatusUpdateRequest(BaseModel):
    user_email: str
    job_id: str


def _sid(doc):
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/register")
def register_disability_user(req: DisabilityRegisterRequest):
    existing = disability_users_col.find_one({"user_email": req.user_email})
    if existing:
        disability_users_col.update_one(
            {"user_email": req.user_email},
            {"$set": {
                "profession": req.profession,
                "disability_type": req.disability_type,
                "skills": req.skills,
                "name": req.name
            }}
        )
        return _sid(disability_users_col.find_one({"user_email": req.user_email}))
    
    doc = {
        "user_email": req.user_email,
        "name": req.name,
        "id_proof": req.id_proof,
        "profession": req.profession,
        "disability_type": req.disability_type,
        "skills": req.skills,
        "total_earnings": 0.0,
        "created_at": datetime.utcnow(),
    }
    result = disability_users_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


@router.post("/post-job")
def post_job(req: PostJobRequest):
    doc = {
        "title": req.title,
        "company": req.company,
        "description": req.description,
        "required_skills": req.required_skills,
        "pay": req.pay,
        "profession": req.profession,
        "status": "open",
        "created_at": datetime.utcnow(),
    }
    result = disability_jobs_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


@router.get("/jobs")
def get_jobs(profession: str = "", user_email: str = ""):
    user_skills = []
    if user_email:
        user = disability_users_col.find_one({"user_email": user_email})
        if user:
            user_skills = user.get("skills", [])
            if not profession:
                profession = user.get("profession", "")

    query = {"status": "open"}
    # We fetch all open jobs and tag them with match metadata
    jobs = list(disability_jobs_col.find(query))
    
    results = []
    for j in jobs:
        j["id"] = str(j.pop("_id"))
        
        # Calculate skill matches
        job_skills = j.get("required_skills", [])
        matches = [s for s in job_skills if s in user_skills]
        j["skill_match_count"] = len(matches)
        j["is_profession_match"] = j.get("profession") == profession
        
        # Heuristic for sorting: profession match > skill match count
        j["match_score"] = (10 if j["is_profession_match"] else 0) + len(matches)
        results.append(j)
    
    # Sort by match score descending
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results


@router.post("/accept")
def accept_job(req: AcceptJobRequest):
    job = disability_jobs_col.find_one({"_id": ObjectId(req.job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.get("status") != "open":
        raise HTTPException(status_code=400, detail="Job is no longer open")

    disability_jobs_col.update_one(
        {"_id": ObjectId(req.job_id)}, 
        {"$set": {"status": "in_progress", "accepted_by": req.user_email, "accepted_at": datetime.utcnow()}}
    )
    return {"message": "Job accepted! Please complete it to receive payment."}


@router.get("/my-active-jobs/{user_email}")
def get_my_active_jobs(user_email: str):
    jobs = list(disability_jobs_col.find({
        "accepted_by": user_email, 
        "status": {"$in": ["in_progress", "completed", "approved"]}
    }))
    for j in jobs:
        j["id"] = str(j.pop("_id"))
    return jobs


@router.post("/complete")
def complete_job(req: StatusUpdateRequest):
    job = disability_jobs_col.find_one({"_id": ObjectId(req.job_id), "accepted_by": req.user_email})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not assigned to you")
    
    disability_jobs_col.update_one(
        {"_id": ObjectId(req.job_id)}, 
        {"$set": {"status": "completed", "completed_at": datetime.utcnow()}}
    )
    return {"message": "Job marked as complete! Waiting for client approval."}


@router.post("/approve")
def approve_job(req: StatusUpdateRequest):
    # In a real app, this would be called by the client/org. 
    # For this demo, we can call it from the UI to show the payment flow.
    job = disability_jobs_col.find_one({"_id": ObjectId(req.job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Only completed jobs can be approved")

    pay = job["pay"]
    user_email = job["accepted_by"]

    # Mark as approved
    disability_jobs_col.update_one(
        {"_id": ObjectId(req.job_id)}, 
        {"$set": {"status": "approved", "approved_at": datetime.utcnow()}}
    )
    
    # Credit the user
    disability_users_col.update_one({"user_email": user_email}, {"$inc": {"total_earnings": pay}})
    
    ledger_col.insert_one({
        "user_email": user_email,
        "type": "credit",
        "amount": pay,
        "description": f"Payment approved for: {job['title']} at {job['company']}",
        "timestamp": datetime.utcnow(),
    })
    
    user = disability_users_col.find_one({"user_email": user_email})
    return {"message": f"₹{pay} credited to worker!", "total_earnings": user["total_earnings"] if user else pay}


@router.get("/revenue/{user_email}")
def get_revenue(user_email: str):
    user = disability_users_col.find_one({"user_email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Also fetch pending earnings
    pending_jobs = list(disability_jobs_col.find({"accepted_by": user_email, "status": "completed"}))
    pending_total = sum(j.get("pay", 0) for j in pending_jobs)
    
    res = _sid(user)
    res["pending_earnings"] = pending_total
    return res
