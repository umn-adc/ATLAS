"""
TODO: 3 steps

1. app = FastAPI()
2. app.include_router(router)
3. @app.get("/health") that returns {"status": "ok"}

Run: uvicorn Workshop.main:app --reload
Test: pytest
"""

from fastapi import FastAPI

from Workshop.router import router

# your code here
