from fastapi import APIRouter ,Body,Path,Query
from .schema import details

routes = APIRouter(tags=["Nested Models"])

@routes.put("/user_full_data")
async def user_data(data : details) -> dict:
    results = {'data':data}
    return results

