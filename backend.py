from fastapi import FastAPI, HTTPException,Request
from main import check_email
import os

app=FastAPI()
WEBHOOK_KEY = os.getenv("WEBHOOK_KEY")

@app.get("/")
def status():
    return{
        "status":"Live..."
    }

@app.get("/check")
def checkMails(request: Request, key: str = None):
    if WEBHOOK_KEY:
        header = request.headers.get("x-api-key")
        if header != WEBHOOK_KEY and key != WEBHOOK_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        check_email()
        return{
            "status":"Up to date.."
        }
    except:
        return{
            "status":"Failed!!!"
        }
    
