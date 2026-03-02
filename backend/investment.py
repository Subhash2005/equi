from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import daily_workers_col, investments_col, ledger_col

router = APIRouter(prefix="/investment", tags=["investment"])

GOLD_PRICE = 6500  # ₹ per gram (simulated)
INVEST_AMOUNT = 100


class InvestRequest(BaseModel):
    user_email: str


class RecoverRequest(BaseModel):
    user_email: str


@router.post("/invest")
def invest(req: InvestRequest):
    worker = daily_workers_col.find_one({"user_email": req.user_email})
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    if worker["balance"] < INVEST_AMOUNT:
        raise HTTPException(status_code=400, detail=f"Insufficient balance. Need ₹{INVEST_AMOUNT}, have ₹{worker['balance']}")

    gold_grams = round(INVEST_AMOUNT / GOLD_PRICE, 6)
    daily_workers_col.update_one({"user_email": req.user_email}, {"$inc": {"balance": -INVEST_AMOUNT, "invested_amount": INVEST_AMOUNT}})

    inv = investments_col.find_one({"user_email": req.user_email})
    if inv:
        investments_col.update_one(
            {"user_email": req.user_email},
            {"$inc": {"total_invested": INVEST_AMOUNT, "gold_grams": gold_grams}}
        )
    else:
        investments_col.insert_one({
            "user_email": req.user_email,
            "total_invested": INVEST_AMOUNT,
            "gold_grams": gold_grams,
            "created_at": datetime.utcnow(),
        })

    ledger_col.insert_one({
        "user_email": req.user_email,
        "type": "debit",
        "amount": INVEST_AMOUNT,
        "description": f"Gold investment: {gold_grams}g @ ₹{GOLD_PRICE}/g",
        "timestamp": datetime.utcnow(),
    })

    worker = daily_workers_col.find_one({"user_email": req.user_email})
    inv = investments_col.find_one({"user_email": req.user_email})
    return {
        "invested": INVEST_AMOUNT,
        "gold_grams": gold_grams,
        "remaining_balance": worker["balance"],
        "total_invested": inv["total_invested"] if inv else INVEST_AMOUNT,
        "total_gold_grams": inv["gold_grams"] if inv else gold_grams,
    }


@router.get("/status/{user_email}")
def get_investment_status(user_email: str):
    inv = investments_col.find_one({"user_email": user_email})
    if not inv:
        return {"total_invested": 0, "gold_grams": 0, "current_value": 0}
    current_value = round(inv["gold_grams"] * GOLD_PRICE * 1.015, 2)
    return {
        "total_invested": inv["total_invested"],
        "gold_grams": inv["gold_grams"],
        "current_value": current_value,
        "appreciation": round(current_value - inv["total_invested"], 2),
    }


@router.post("/recover")
def recover(req: RecoverRequest):
    inv = investments_col.find_one({"user_email": req.user_email})
    if not inv or inv.get("total_invested", 0) == 0:
        raise HTTPException(status_code=400, detail="No investments to recover")

    recovered = round(inv["total_invested"] * 1.015, 2)
    daily_workers_col.update_one(
        {"user_email": req.user_email},
        {"$inc": {"balance": recovered}, "$set": {"invested_amount": 0}}
    )
    investments_col.update_one(
        {"user_email": req.user_email},
        {"$set": {"total_invested": 0, "gold_grams": 0}}
    )
    ledger_col.insert_one({
        "user_email": req.user_email,
        "type": "credit",
        "amount": recovered,
        "description": "Emergency gold recovery (1.5% appreciation)",
        "timestamp": datetime.utcnow(),
    })
    worker = daily_workers_col.find_one({"user_email": req.user_email})
    return {"recovered_amount": recovered, "new_balance": worker["balance"]}
