import re

from pydantic import BaseModel, validator


class Email(BaseModel):
    username: str
    password: str
    smtp_server: str
    smtp_port: int

    @validator('username')
    def email(cls, value):
        try:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', value).group()
        except AttributeError:
            raise ValueError(f"{value} isn't valid email")
        return value