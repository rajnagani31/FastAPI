from fastapi.responses import JSONResponse,Response
from typing import Annotated 
from fastapi import Header, HTTPException
async def get_query_param(q: str | None = None , name :str |None = None) -> dict:
    return JSONResponse(status_code=201, content={"q": q, "name": name})


import asyncio
class CheakAsyncioMetod:
    async def cheak(self):
        await asyncio.sleep(2)
        print('1')
        # return Response(content="Cheak Asyncio Metod", media_type="text/plain")
        # return JSONResponse(status_code=200, content={"message": "Cheak  Method"})
        data= {"message": "Cheak  Method"}
        return data
    
    async def cheak_again(self):
        await asyncio.sleep(1)
        print('2')
        data = {"message": "Cheak Again Method"}
        return data
    
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key