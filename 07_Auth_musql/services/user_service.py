from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from model.user_auth import UserAuth,UserToken
import logging
import hashlib
from fastapi.responses import JSONResponse
from fastapi import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

def get_hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()





def create_user(username: str, email: str, password: str, db: Session):
    try:
        user = UserAuth(
            username=username,
            email=email,
            hashed_password=get_hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"User created with id={user.id}")
        return user

    except IntegrityError:
        db.rollback()
        raise ValueError("User already exists")

    except Exception as e:
        db.rollback()
        logger.exception("Error creating user")
        raise


def get_user_by_email(email: str, hashed_password: str, db: Session):
    return db.query(UserAuth).filter(UserAuth.email == email, UserAuth.hashed_password == hashed_password).first()

def insert_token(user_id: int, token: str, db: Session):
    try:
        # Upsert query can be implemented here
        user_token = db.query(UserToken).filter(UserToken.user_id == user_id).first()
        if user_token:
            user_token.token = token
            user_token.is_deleted = False
        else:
            user_token = UserToken(user_id=user_id, token=token)
            db.add(user_token)

        db.commit()
        db.refresh(user_token)

        logger.info(f"Token inserted for user_id={user_id}")
        return user_token

    except Exception as e:
        db.rollback()
        logger.exception("Error inserting token")
        raise


def update_password(user_id: int, new_password: str, db: Session):
    try:
        user = db.query(UserAuth).filter(UserAuth.id == user_id).first()
        if user:
            user.hashed_password = get_hash_password(new_password)
            db.commit()
            db.refresh(user)
            logger.info(f"Password updated for user_id={user_id}")

            return user
        else:
            return None

    except Exception as e:
        db.rollback()
        logger.exception("Error updating password")
        raise


def logout_user(user_id: int, db: Session):
    try:
        user_token = db.query(UserToken).filter(UserToken.user_id == user_id).first()
        if user_token:
            user_token.is_deleted = True
            db.commit()
            db.refresh(user_token)
            logger.info(f"User logged out with user_id={user_id}")
            return user_token
        else:
            return None

    except Exception as e:
        db.rollback()
        logger.exception("Error logging out user")
        raise