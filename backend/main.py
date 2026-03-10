import os
import sys

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Add the parent directory (project root) to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
import uvicorn

app = FastAPI(title="SignSight Vision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(os.path.join(ROOT_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, "outputs"), exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, "models"), exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "frontend", "static")), name="static")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
