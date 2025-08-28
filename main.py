from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import resend
import traceback

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Resend API key
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if not RESEND_API_KEY:
    print("⚠️ WARNING: RESEND_API_KEY not set in environment!")
else:
    resend.api_key = RESEND_API_KEY


# Request model
class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str


@app.post("/send-email")
def send_email(email: EmailRequest):
    try:
        params: resend.Emails.SendParams = {
            "from": "Resend <onboarding@resend.dev>",  # must use Resend verified domain
            "to": [email.to],
            "subject": email.subject,
            "html": email.html,
        }
        response = resend.Emails.send(params)
        return {"success": True, "response": response}
    except Exception as e:
        print("❌ ERROR:", traceback.format_exc())
        return {"success": False, "error": str(e)}


@app.get("/")
def root():
    return {"message": "🚀 Resend Email API running!"}
