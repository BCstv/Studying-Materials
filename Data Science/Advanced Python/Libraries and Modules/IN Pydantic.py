from pydantic import BaseModel
class User(BaseModel):
    first_name: str
    last_name: str

a = User(first_name="Smith", last_name="Adam")
print(a)
