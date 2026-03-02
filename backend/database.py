from pymongo import MongoClient
from pymongo.collection import Collection
import os

# Load .env file if present (for local dev)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use environment variables directly

# ── Connection ────────────────────────────────────────────────────────────────

# 🔥 IMPORT THIS FROM RENDER ENV or .env
# Must set MONGO_URI in Render environment variables
# Format example (Atlas):
# mongodb+srv://USERNAME:PASSWORD@yourcluster.mongodb.net/equibridge?retryWrites=true&w=majority
MONGO_URI = os.getenv("MONGO_URI")  # <-- USE THIS instead of localhost

print(f"🔌 Connecting to MongoDB: {MONGO_URI}...") 

# client tries to connect to cloud MongoDB Atlas or other remote URL
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Test connection
try:
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("   Check that your MONGO_URI environment variable is set correctly.")

# ── Database & Collections ────────────────────────────────────────────────────

db = client["equibridge"]

users_col: Collection = db["users"]
students_col: Collection = db["students"]
organizations_col: Collection = db["organizations"]
work_listings_col: Collection = db["work_listings"]
daily_workers_col: Collection = db["daily_workers"]
investments_col: Collection = db["investments"]
disability_users_col: Collection = db["disability_users"]
disability_jobs_col: Collection = db["disability_jobs"]
ledger_col: Collection = db["ledger"]

def create_indexes():
    try:
        users_col.create_index("email", unique=True)
        students_col.create_index("user_email", unique=True)
        daily_workers_col.create_index("user_email", unique=True)
        disability_users_col.create_index("user_email", unique=True)
        organizations_col.create_index([("field", 1), ("name", 1)])
    except Exception as e:
        print(f"⚠️ Index creation warning: {e}")
