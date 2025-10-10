from sqlalchemy.orm import Session
import schema , model


def Create_user(db : Session , user: schema.CreateUser):
    db_user = model.User(email = user.email , name = user.name , age = user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db : Session):
    return db.query(model.User).all()

def get_user(db: Session , id : int):
    user =  db.query(model.User).filter(model.User.id == id).first()

    return user

def user_delete(db: Session, id: int):
    user_delete = db.query(model.User).filter(model.User.id == id).first()
    if user_delete:
        db.delete(user_delete)
        db.commit()
        return True
    return False

def update_user_details(db: Session , user: schema.UserBase , id : int ):
    print(id)
    user_update = db.query(model.User).filter(model.User.id == id).first()
    print(user_update)
    if  user_update is None:
        return False
    user_update.name = user.name
    user_update.age = user.age
    user_update.email = user.email
    db.commit()
    return True

