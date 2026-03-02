from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from database import students_col, organizations_col, ledger_col
from curriculum import get_curriculum

router = APIRouter(prefix="/student", tags=["student"])


class StudentRegisterRequest(BaseModel):
    user_email: str
    name: str
    age: int
    document_id: str
    field_of_interest: str


class ProgressUpdateRequest(BaseModel):
    user_email: str
    org_name: str
    completed_steps: List[int]


class QuizSubmitRequest(BaseModel):
    user_email: str
    month: int
    answers: List[int]          # index of chosen option per question
    task_submission: str = ""   # text/link submitted for the practical task


class RepaymentRequest(BaseModel):
    user_email: str


def _serialize(doc):
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/register")
def register_student(req: StudentRegisterRequest):
    existing = students_col.find_one({"user_email": req.user_email})
    if existing:
        return {"message": "Existing student found", **_serialize(existing)}

    doc = {
        "user_email": req.user_email,
        "name": req.name,
        "age": req.age,
        "document_id": req.document_id,
        "field_of_interest": req.field_of_interest,
        "selected_org": None,
        "completed_steps": [],
        "total_funding_received": 0,
        "job_placed": False,
        "salary": 50000,
        "repayment_paid": 0,       # total repaid so far
        "months_repaid": 0,        # how many months of repayment done
        "quiz_results": {},        # month -> {score, passed, task_submitted}
        "created_at": datetime.utcnow(),
    }
    result = students_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return {"message": "Student registered", **doc}


@router.get("/me/{user_email}")
def get_student(user_email: str):
    student = students_col.find_one({"user_email": user_email})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return _serialize(student)


@router.get("/organizations")
def get_organizations(field: str = ""):
    query = {"field": field} if field else {}
    orgs = list(organizations_col.find(query, {"roadmap": 0}))
    for org in orgs:
        org["id"] = str(org.pop("_id"))
    return orgs


@router.get("/pipeline/{org_name}")
def get_pipeline(org_name: str):
    org = organizations_col.find_one({"name": org_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    org["id"] = str(org.pop("_id"))
    return org


@router.post("/select-org")
def select_org(user_email: str, org_name: str):
    org = organizations_col.find_one({"name": org_name})
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")
    students_col.update_one(
        {"user_email": user_email},
        {"$set": {"selected_org": org_name, "completed_steps": [], "total_funding_received": 0}}
    )
    return {"message": f"Joined {org_name}", "org": org_name}


@router.post("/progress")
def update_progress(req: ProgressUpdateRequest):
    org = organizations_col.find_one({"name": req.org_name})
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")

    # Org funds 100% — student pays nothing. Calculate total funding from completed steps.
    total_funding = 0
    for step in org.get("roadmap", []):
        if step["step"] in req.completed_steps:
            # All fees funded by org — student cost = 0
            total_funding += step.get("estimated_fee", 0)

    total_steps = len(org.get("roadmap", []))
    pct = round(len(req.completed_steps) / total_steps * 100) if total_steps else 0

    students_col.update_one(
        {"user_email": req.user_email},
        {"$set": {
            "completed_steps": req.completed_steps,
            "total_funding_received": total_funding,
            "progress_pct": pct,
        }}
    )
    return {
        "completed_steps": req.completed_steps,
        "total_funding_received": total_funding,
        "progress_pct": pct,
        "total_steps": total_steps,
    }


# ── Quiz & Task Endpoints ──────────────────────────────────────────────────────

@router.get("/curriculum/{field}")
def get_curriculum_for_field(field: str):
    """Return monthly quiz + task curriculum for a given field."""
    curriculum = get_curriculum(field)
    # Strip correct answers before sending to frontend
    safe = []
    for month_data in curriculum:
        quiz_safe = [{"q": q["q"], "options": q["options"]} for q in month_data["quiz"]]
        safe.append({
            "month": month_data["month"],
            "topic": month_data["topic"],
            "quiz": quiz_safe,
            "task": month_data["task"],
        })
    return safe


@router.post("/quiz/submit")
def submit_quiz(req: QuizSubmitRequest):
    """Submit quiz answers and task for a given month. Returns score and pass/fail."""
    student = students_col.find_one({"user_email": req.user_email})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    field = student.get("field_of_interest", "Software Developer")
    curriculum = get_curriculum(field)

    # Find the month
    month_data = next((m for m in curriculum if m["month"] == req.month), None)
    if not month_data:
        raise HTTPException(status_code=404, detail=f"Month {req.month} curriculum not found")

    # Grade the quiz
    correct_answers = [q["answer"] for q in month_data["quiz"]]
    score = sum(1 for i, ans in enumerate(req.answers) if i < len(correct_answers) and ans == correct_answers[i])
    total_q = len(correct_answers)
    pct_score = round(score / total_q * 100)
    passed = pct_score >= 60  # 60% to pass

    result = {
        "month": req.month,
        "topic": month_data["topic"],
        "score": score,
        "total": total_q,
        "pct_score": pct_score,
        "passed": passed,
        "task_submitted": bool(req.task_submission),
        "task_submission": req.task_submission,
        "submitted_at": datetime.utcnow().isoformat(),
    }

    # Save result
    students_col.update_one(
        {"user_email": req.user_email},
        {"$set": {f"quiz_results.month_{req.month}": result}}
    )

    return {
        "score": score,
        "total": total_q,
        "pct_score": pct_score,
        "passed": passed,
        "correct_answers": correct_answers,
        "message": "✅ Passed! Great work." if passed else "❌ Failed. Score 60%+ to pass. Try again next month.",
    }


@router.get("/quiz/results/{user_email}")
def get_quiz_results(user_email: str):
    student = students_col.find_one({"user_email": user_email})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.get("quiz_results", {})


# ── Job Status & Repayment ────────────────────────────────────────────────────

@router.get("/job-status/{user_email}")
def get_job_status(user_email: str):
    student = students_col.find_one({"user_email": user_email})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    org_name = student.get("selected_org", "")
    org = organizations_col.find_one({"name": org_name}) if org_name else None

    salary = student.get("salary", 50000)
    total_funding = student.get("total_funding_received", 0)
    repayment_paid = student.get("repayment_paid", 0)
    months_repaid = student.get("months_repaid", 0)

    # 10% of salary per month until fully repaid
    monthly_repayment = round(salary * 0.10)
    remaining_debt = max(0, total_funding - repayment_paid)
    months_remaining = (remaining_debt // monthly_repayment + 1) if remaining_debt > 0 else 0
    net_this_month = salary - (monthly_repayment if remaining_debt > 0 else 0)

    # Build step-by-step funding breakdown
    funding_breakdown = []
    if org:
        for step in org.get("roadmap", []):
            if step["step"] in student.get("completed_steps", []):
                funding_breakdown.append({
                    "step": step["step"],
                    "title": step["title"],
                    "org_funded": step.get("estimated_fee", 0),
                    "student_paid": 0,  # org funds 100%
                })

    students_col.update_one({"user_email": user_email}, {"$set": {"job_placed": True}})

    return {
        "name": student.get("name", ""),
        "org": org_name,
        "field": student.get("field_of_interest", ""),
        "salary": salary,
        "total_funding_received": total_funding,
        "repayment_paid": repayment_paid,
        "remaining_debt": remaining_debt,
        "monthly_repayment": monthly_repayment,   # 10% of salary
        "months_repaid": months_repaid,
        "months_remaining": months_remaining,
        "net_this_month": net_this_month,
        "funding_breakdown": funding_breakdown,
        "completed_steps": student.get("completed_steps", []),
        "progress_pct": student.get("progress_pct", 0),
    }


@router.post("/repay-month")
def repay_month(req: RepaymentRequest):
    """Record one month's repayment (10% of salary)."""
    student = students_col.find_one({"user_email": req.user_email})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    salary = student.get("salary", 50000)
    monthly_repayment = round(salary * 0.10)
    total_funding = student.get("total_funding_received", 0)
    repayment_paid = student.get("repayment_paid", 0)
    remaining = max(0, total_funding - repayment_paid)

    if remaining <= 0:
        return {"message": "Debt fully repaid! 🎉", "remaining_debt": 0}

    actual_payment = min(monthly_repayment, remaining)
    new_paid = repayment_paid + actual_payment
    new_remaining = max(0, total_funding - new_paid)

    students_col.update_one(
        {"user_email": req.user_email},
        {"$inc": {"repayment_paid": actual_payment, "months_repaid": 1}}
    )

    ledger_col.insert_one({
        "user_email": req.user_email,
        "type": "debit",
        "amount": actual_payment,
        "description": f"Monthly fund repayment to {student.get('selected_org', 'org')} (10% of salary)",
        "timestamp": datetime.utcnow(),
    })

    return {
        "paid_this_month": actual_payment,
        "total_paid": new_paid,
        "remaining_debt": new_remaining,
        "message": "✅ Payment recorded" if new_remaining > 0 else "🎉 Debt fully repaid!",
    }
