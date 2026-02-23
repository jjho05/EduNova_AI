"""
Sanity Check Script
Run this to verify basic system health before deployment.
Usage: python tests/sanity_check.py
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from sqlalchemy import text

def test_database_connection():
    print("🔌 Testing Database Connection...")
    try:
        db = SessionLocal()
        # Try a simple query
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_api_health():
    print("\n🏥 Testing API Health...")
    client = TestClient(app)
    try:
        response = client.get("/api/health")
        if response.status_code == 200:
            print(f"✅ API Health Check passed: {response.json()}")
            return True
        else:
            print(f"❌ API Health Check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Request failed: {e}")
        return False

def run_sanity_check():
    print("🚀 Starting Pre-Flight Sanity Check\n" + "="*30)
    
    db_ok = test_database_connection()
    api_ok = test_api_health()
    
    print("\n" + "="*30)
    if db_ok and api_ok:
        print("🎉 SYSTEM READY FOR LIFT-OFF!")
        sys.exit(0)
    else:
        print("💥 SYSTEM HEALTH CRITICAL - DO NOT DEPLOY")
        sys.exit(1)

if __name__ == "__main__":
    run_sanity_check()
