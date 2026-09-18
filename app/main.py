from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.auth import auth_service
from app.wallet import wallet
from app.payments import payment_service
from app.predictor import router as predictor_router
# Import the brand new internet agent router
from app.agent_engine import router as agent_router
from app.database import init_db
import os

init_db()

app = FastAPI(title="AI Soccer Analyzer API")

app.include_router(auth_service.router)
app.include_router(wallet.router)
app.include_router(payment_service.router)
app.include_router(predictor_router)
# Register the agent endpoints into the system map
app.include_router(agent_router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as file:
        return file.read()
