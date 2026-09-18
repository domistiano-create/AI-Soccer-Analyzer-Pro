from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.auth import auth_service
from app.wallet import wallet
from app.payments import payment_service
from app.predictor import router as predictor_router
from app.agent_engine import router as agent_router
from app.database import init_db
import os

# Initialize storage tables row configurations immediately at start
init_db()

app = FastAPI(title="AI Soccer Analyzer API")

# Mount your application core functional feature tracks
app.include_router(auth_service.router)
app.include_router(wallet.router)
app.include_router(payment_service.router)
app.include_router(predictor_router)
app.include_router(agent_router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the interactive frontend web interface layout safely on both cloud and local setups."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try local root pathing option first
    html_path = os.path.join(current_dir, "app", "index.html")
    
    # Cloud Fail-safe fallback if already running inside the app namespace folder directory
    if not os.path.exists(html_path):
        html_path = os.path.join(current_dir, "index.html")
        
    with open(html_path, "r", encoding="utf-8") as file:
        return file.read()
