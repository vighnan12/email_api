from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import resend
import traceback

app = FastAPI()

# Enable CORS for frontend usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Resend API Key
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if not RESEND_API_KEY:
    print("⚠️ ERROR: RESEND_API_KEY not set in environment!")
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
        # ✅ Send email with Resend
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",   # Sandbox sender
            "to": [email.to],
            "subject": email.subject,
            "html": email.html,
        })

        return {"success": True, "response": response}

    except Exception as e:
        tb = traceback.format_exc()
        print("❌ ERROR:", tb)
        return {"success": False, "error": str(e), "traceback": tb}


@app.get("/")
def root():
    return {"message": "🚀 Resend Email API is running!"}
