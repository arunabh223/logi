import resend
import os
from dotenv import load_dotenv
load_dotenv()

def send_mail(content: str, vendors: list):
    resend_api_key = os.getenv("RESEND_API_KEY")
    if not resend_api_key:
        raise ValueError("RESEND_API_KEY environment variable is not set.") 
    
    resend.api_key = resend_api_key
    
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": vendors,
        "subject": "Request for material",
        "html": content,
    }

    response = resend.Emails.send(params)
    return response

if __name__ == "__main__":
    # with open("rfq_document.md", "r") as file:
    #     rfq_content = file.read()
    rfq_content = "Please send the material as soon as possible."
    vendors = ["delivered@resend.dev", "arunabh223@gmail.com"]
    try:
        response = send_mail(rfq_content, vendors)
        print("Email sent successfully:", response)
    except Exception as e:
        print("Failed to send email:", str(e))