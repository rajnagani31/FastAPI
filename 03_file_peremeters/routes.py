from fastapi import APIRouter ,File ,UploadFile ,Depends ,Form ,HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from schema import UserFileDataBase , UserSchema
from database import get_db
from model import User_details ,User_file_data
from fastapi.exceptions import RequestValidationError
routrs = APIRouter(tags=["User File data"])


@routrs.post("/User_file")
async def user_upload_file(user_id : int , File : Annotated[bytes , File()]):
    user_data = {"user_id":user_id , "file":len(File)}
    return user_data


def human_readable(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.0f} PB"


@routrs.post("/user_multiple_file")
async def user_upload_multiple_file(user_id: int , File :list[UploadFile]  = File()):
    file_data = []
    for data in File:
        with open(data.filename , "wb") as f:
            f.write(await data.read())

        type = data.content_type
        name = data.filename
        file_size = data.size
        file_data.append({"file_name":name , "File_type":type , "Size":file_size ,"Size_readable":str(human_readable(file_size))})

    return {
        "user_id":user_id,
        "data":file_data    
    }



@routrs.post("/user-Create")
async def create_user(user : UserSchema , db:Session = Depends(get_db)):
    db_user = User_details(user_name = user.user_name , created_at = user.created_at , updated_at = user.updated_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"User is Created Successfuly"}




@routrs.post("/user_file_upload_with_Db" )
async def user_file_info(user_id: int, File: list[UploadFile] = File() , db : Session = Depends(get_db)):
    
    for data in File:
        read = data.read()
        print("read:",read)
        file_name = data.filename
        type = data.content_type
        # size = data.size
        file_bytes = await data.read()  # ✅ read bytes from uploaded file
        file_size = len(file_bytes)
        db_user = User_file_data(user_id = user_id , file_name = file_name ,file_type = type ,
                                 file_size = file_size , size_readable = str(human_readable(file_size)) , file_data = file_bytes)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"Message": "Data created Successfully"}

@routrs.get("/get_user_file/data")
async def get_user_file_data(user_id :int,db: Session = Depends(get_db)):
    data = db.query(User_file_data).filter(User_file_data.user_id == user_id).all()
    return data



from fastapi.responses import StreamingResponse
from io import BytesIO

@routrs.get("/user_file_download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(User_file_data).filter(User_file_data.id == file_id).first()
    if not file_record:
        raise  HTTPException(status_code=404, detail="File not found")

    # Create a file-like object from the binary data
    file_stream = BytesIO(file_record.file_data)    

    # Send as downloadable file
    return StreamingResponse(
        file_stream,
        media_type=file_record.file_type,
        headers={"Content-Disposition": f"attachment; filename={file_record.file_name}"}
    )


def generate_numbers():
    for i in range(1, 6):
        yield f"Number: {i}\n"

@routrs.get("/numbers")
def stream_numbers():
    return StreamingResponse(generate_numbers(), media_type="text/plain")