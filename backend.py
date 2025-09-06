from fastapi import FastAPI
from main import check_email

app=FastAPI()

@app.get("/")
def status():
    return{
        "status":"Live..."
    }

@app.get("/check")
def checkMails():
    try:
        check_email()
        return{
            "status":"Up to date.."
        }
    except:
        return{
            "status":"Failed!!!"
        }
    
