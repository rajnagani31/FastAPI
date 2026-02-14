# Gloabl dependencies

from fastapi import APIRouter , Depends
from depens import CheakAsyncioMetod
import asyncio
from fastapi.responses import JSONResponse,Response
from depens import verify_token, verify_key

router = APIRouter(tags=['Gloabel Dependencies'], dependencies=[Depends(verify_key), Depends(verify_token)])

cheak_asyncio = CheakAsyncioMetod()

@router.post("/decoretor_depends")
async def cheak_token():
    function = await asyncio.gather(
        cheak_asyncio.cheak(),
        cheak_asyncio.cheak_again()
    )
    data =[f for f in function]
    print(data)
    return JSONResponse(status_code=200 , content={"data":data , "Token": "Valid token and secret key"}, media_type="application/json")