from typing import Union
import uvicorn
from fastapi import FastAPI, status
from baseModels import ResponseBad, ResponseOk

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK, response_model=Union[ResponseOk, ResponseBad])
async def index():
    return {"message": "Custom Response", "status": status.HTTP_200_OK, "data": {}}


if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost")
