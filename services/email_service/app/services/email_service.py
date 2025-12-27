from ..schemas.email import EmailSchema
from fastapi_mail import FastMail


class EmailService:
    
    @classmethod 
    async def send_email(email: EmailSchema) -> None:
        
        fm = FastMail() # TODO: Create and add configurations insde the fastmail
        await fm.send_email() # TODO: Create email recipient
    
        