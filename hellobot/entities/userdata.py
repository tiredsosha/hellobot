import re
from pydantic import BaseModel, validator


class Userdata(BaseModel):
    credentials: dict
    users: list

    @validator('credentials')
    def cred(cls, value):
        for v, k in value.items():
            if k == None or k == '':
                raise ValueError(f"{v} is empty")
        return value

    @validator('users')
    def user(cls, value):
        for email in value:
            try:
                email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', email).group()
            except AttributeError:
                raise ValueError(f"{email} isn't valid email")
        return value


def from_dict(data: dict):
    userdata = {}
    for k, v in data.items():
        userdata[k] = Userdata(**v)
    return userdata
