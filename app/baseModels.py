from pydantic import BaseModel
from typing import Union, Optional
from fastapi import status


class ResponseOk(BaseModel):
    message: str = "ok"
    status: int = status.HTTP_200_OK
    data: Union[dict, list]

class ResponseBad(BaseModel):
    message: str = "Not Found"
    status: int = status.HTTP_404_NOT_FOUND
    data: Optional[dict] = None

