from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


class Msg(BaseModel):
    msg: str

    class Config:
        orm_mode = True
