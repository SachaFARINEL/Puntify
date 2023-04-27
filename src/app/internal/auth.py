import os
from datetime import timedelta, datetime
from jose import jwt
from passlib.context import CryptContext

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # create jwt token
    to_encode = data.copy()
    # set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=float(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    # add expiration time to jwt token
    to_encode.update({"exp": expire})
    # encode jwt token
    encoded_jwt = jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])

    return encoded_jwt
