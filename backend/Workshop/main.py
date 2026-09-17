"""
TODO: 3 steps

1. app = FastAPI()
2. app.include_router(router)
3. @app.get("/health") that returns {"status": "ok"}

Run: uvicorn Workshop.main:app --reload
Test: run `pytest -v --tb=no` from atlas/backend
"""

from fastapi import FastAPI

from Workshop.router import router

# your code here...

app = FastAPI()

app.include_router(router)

@app.get("/health")
def get_health():
    return {"status": "ok"}