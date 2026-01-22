from fastapi import APIRouter


router = APIRouter(
    prefix="/v1/admin",
    tags=['admin']
)

@router.get('/get-user-list')
async def get_all_user_detail():
    pass