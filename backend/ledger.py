from fastapi import APIRouter, HTTPException
from database import ledger_col

router = APIRouter(prefix="/ledger", tags=["ledger"])


@router.get("/{user_email}")
def get_ledger(user_email: str):
    entries = list(ledger_col.find({"user_email": user_email}).sort("timestamp", -1).limit(50))
    for e in entries:
        e["id"] = str(e.pop("_id"))
        if "timestamp" in e:
            e["timestamp"] = e["timestamp"].isoformat()
    return entries
