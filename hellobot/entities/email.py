from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError


class Email(BaseModel):
    username: str
    password: str
    smtp_server: str
    smtp_port: int

    @validator('username')
    def email(cls, value):
        try:
            valid = validate_email(value)
        except EmailNotValidError:
            raise ValueError(f"{value} isn't valid email")
        return value