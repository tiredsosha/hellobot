from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError


class Users(BaseModel):
    developers: list
    designers: list
    finance: list
    tech: list
    marketing: list
    manager: list
    admin: list
    office: list
    hr: list
    test: list
    sapozhnikova: str
    dyubarov: str
    korchagina: str

    @validator('*')
    def email(cls, value):
        if isinstance(value, list):
            for email in value:
                try:
                    valid = validate_email(email)
                except EmailNotValidError:
                    raise ValueError(f"{email} isn't valid email")
        else:
            try:
                valid = validate_email(value)
            except EmailNotValidError:
                raise ValueError(f"{value} isn't valid email")
        return value
