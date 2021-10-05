from pydantic import BaseModel, validator
import yaml
import re


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
                    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', email).group()
                except AttributeError:
                    raise ValueError(f"{email} isn't valid email")
        else:
            try:
                email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', value).group()
            except AttributeError:
                raise ValueError(f"{value} isn't valid email")
        return value


with open('configs/user.yaml') as users:
    users = Users(**yaml.safe_load(users))

email = 'p@gmail.com'

for it in users:
    if email in it[1]:
        key = it[0]
    else:
        key = 'no'
    print(key)