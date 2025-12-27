from fastapi import FastAPI 
from api.v1.api import router
app = FastAPI(
    title="NeuroFlow Email Service", 
    version="0.0.1", 
    summary="Service to send email for NeuroFlow users to communicate with promo, notifications, authentication and etc.",
    tags=["Email Service"]
)




@app.get("/health")
async def health_check():
    """Health check endpoint for the email service."""
    return {"status":"healthy"}




app.include_router(router)
