from fastapi import Depends, HTTPException, APIRouter,Response,Cookie,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from typing import Annotated
from ..Crud import user_crud
from ..Services import auth_service
from .. import schemas,database,models
from .. import dependencies


router =APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if user_crud.get_user_by_username(db, user.username) or user_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    if user.user_type not in [models.UserType.simple, models.UserType.photographer]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    return user_crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(response: Response,form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token_data = {"sub": str(user.id)}
    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(token_data)

    response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite="lax",max_age=900)
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite="lax",max_age=604800)

    return schemas.Token(access_token=access_token,refresh_token=refresh_token,token_type="bearer")

@router.get("/logout")
def logout(response: Response,current_user:Session=Depends(dependencies.get_current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if(current_user):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Logged out"}
    else:
        raise credentials_exception
    
@router.get("/refresh")
def refresh(response:Response ,request:Request,current_user:Session=Depends(dependencies.get_current_user)):
    refresh_token = request.cookies.get("access_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    token_data = {"sub": str(current_user.id)}
    access_token = auth_service.create_access_token(token_data)
    refresh_token_new = auth_service.create_refresh_token(token_data)

    response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite="lax",max_age=1800)
    response.set_cookie("refresh_token", refresh_token_new, httponly=True, secure=False, samesite="lax",max_age=604800)

    return {
        "refresh_token": refresh_token,
        "message":"Token refresh"
            }

# @router.post("/logout")
# def logout(db:Session=Depends(database.get_db),token:str=Depends(dependencies.oauth2_scheme),current_user=Depends(dependencies.get_current_active_user)):
#     try:
#         # Add current token to blacklist
#         user_crud.blacklist_token(db, token)
        
#         return {
#             "message": "Successfully logged out",
#             "status": "success",
#             "user_id": current_user.id,
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Logout failed")

