import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.database import init_db
import uvicorn
import traceback

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Debug endpoint to test functionality
@app.post("/api/debug/signup")
def debug_signup(full_name: str, email: str, password: str):
    from src.auth.signup_service import signup_user
    from src.database import get_session
    try:
        gen = get_session()
        db = next(gen)
        result = signup_user(db, full_name, email, password)
        next(gen, None)  # Close the session
        return result
    except Exception as e:
        next(gen, None)  # Close the session
        print(f"Debug signup error: {e}")
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)