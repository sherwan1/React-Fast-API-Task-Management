
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.dependencies import get_db
from app.models import User
from app.schemas import UserRequest, UserResponse, user


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    
    if(user_id <= 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Id is not valid.")
    
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        return user
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")

@router.post("/", response_model=UserResponse)
def post_user(request: UserRequest, db: Session = Depends(get_db)):
    if "@" not in request.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email format")

    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    response = User(name = request.name,
                    email = request.email,
                    password = request.password)

    try:
        db.add(response)
        db.commit()
        db.refresh(response)

        return response
    except Exception:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, request: UserRequest, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is not valid")
    
    existing_user = db.query(User).filter(User.id == user_id).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User doesn't exist")

    existing_user.name = request.name
    existing_user.email = request.email
    existing_user.password = request.password

    try:
        db.commit()
        db.refresh(existing_user)

        return existing_user
    except Exception:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be updated")

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is not valid")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist to delete")
    
    try:
        db.delete(user)
        db.commit()
    
        return {
            "message": f"User {user_id} is deleted successfully"
        }
    
    except Exception:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"User {user_id} could not be deleted")










    

    