from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import resend

app = FastAPI()

# Allow CORS from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from environment variable
resend.api_key = os.getenv("RESEND_API_KEY")

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str

@app.post("/send-email")
async def send_email(email: EmailRequest):
    try:
        params: resend.Emails.SendParams = {
            "from": "Your Name <you@yourverifieddomain.com>",  # must be verified in Resend
            "to": [email.to],
            "subject": email.subject,
            "html": email.html,
        }
        response = resend.Emails.send(params)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
async def root():
    return {"message": "Resend Email API running 🚀"}
