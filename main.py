from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import resend
import traceback

app = FastAPI()

#  Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Load Resend API Key
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if not RESEND_API_KEY:
    raise RuntimeError("RESEND_API_KEY not set in environment.")
resend.api_key = RESEND_API_KEY

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str

@app.post("/send-email")
def send_email(email: EmailRequest):
    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",     # sandbox-safe sender
            "to": [email.to],
            "subject": email.subject,
            "html": email.html,
        })
        return {"success": True, "response": response}
    except resend.exceptions.ResendError as re_error:
        # Capture Resend-specific errors (like rate limit, quota, etc.)
        error_details = repr(re_error)
        print("💥 ResendError traceback:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail={
            "success": False,
            "error": "ResendError",
            "message": error_details
        })
    except Exception as e:
        # Catch any other unexpected exceptions
        print("💥 General Error traceback:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail={
            "success": False,
            "error": "UnknownError",
            "message": str(e)
        })

@app.get("/")
def root():
    return {"message": "🚀 Resend Email API is running!"}
