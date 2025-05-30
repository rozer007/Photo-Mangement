from fastapi import Depends, HTTPException, APIRouter,Response,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Optional
from typing import Annotated
from ..Crud import user_crud
from ..Services import auth_service
from .. import schemas,database,models
from .. import dependencies
from ..Services import magic_link_service


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
        response.delete_cookie("magic_token")
        return {"message": "Logged out"}
    else:
        raise credentials_exception
    
@router.get("/refresh")#,include_in_schema=False)
def refresh(response:Response ,request:Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    user_id=auth_service.verify_token(refresh_token)

    token_data = {"sub": str(user_id)}
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


@router.post('/magic_link')
def magic_login_link(response:Response,email:str,db:Session=Depends(database.get_db)):
    user=user_crud.get_user_by_email(db,email)

    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please register first."
                )
    
    token,magic_link_url=magic_link_service.generate_magic_link(email,db)
    response.set_cookie("magic_token", token, httponly=True, secure=False, samesite="lax",max_age=600)


    return {
            "Token": token,
            "magic_link":magic_link_url,
            "email": email
    }


# hidden endpoint
@router.get('/verify_magic_login',response_model=schemas.Token)#,include_in_schema=False)
def magic_login(request:Request,response:Response,db:Session=Depends(database.get_db)):

    magic_token= refresh_token = request.cookies.get("magic_token")
    print(magic_token)
    email=magic_link_service.verify_magic_token(magic_token,db)

    user=user_crud.get_user_by_email(db,email)

    token_data = {"sub": str(user.id)}

    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(token_data)

    response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite="lax",max_age=900)
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite="lax",max_age=604800)

    # result=RedirectResponse(url='http://127.0.0.1:8000')

    return schemas.Token(access_token=access_token,refresh_token=refresh_token,token_type="bearer")

