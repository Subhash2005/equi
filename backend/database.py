from pymongo import MongoClient
from pymongo.collection import Collection
import os

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use environment variables directly

# ── Connection ─────────────────────────────────────────────────────────────────
# Default: local MongoDB (works with Compass on localhost:27017)
# Override by setting MONGO_URI in backend/.env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

print(f"🔌 Connecting to MongoDB: {MONGO_URI[:40]}...")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Test connection
try:
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("   Make sure MongoDB is running: mongod --dbpath C:\\data\\db")

db = client["equibridge"]

# ── Collections ────────────────────────────────────────────────────────────────
users_col: Collection = db["users"]
students_col: Collection = db["students"]
organizations_col: Collection = db["organizations"]
work_listings_col: Collection = db["work_listings"]
daily_workers_col: Collection = db["daily_workers"]
investments_col: Collection = db["investments"]
disability_users_col: Collection = db["disability_users"]
disability_jobs_col: Collection = db["disability_jobs"]
ledger_col: Collection = db["ledger"]

# ── Indexes ────────────────────────────────────────────────────────────────────
def create_indexes():
    try:
        users_col.create_index("email", unique=True)
        students_col.create_index("user_email", unique=True)
        daily_workers_col.create_index("user_email", unique=True)
        disability_users_col.create_index("user_email", unique=True)
        organizations_col.create_index([("field", 1), ("name", 1)])
    except Exception as e:
        print(f"⚠️  Index creation warning: {e}")
