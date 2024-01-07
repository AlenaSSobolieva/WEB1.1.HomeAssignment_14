# app/routes.py

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from cloudinary.uploader import upload
import crud, database, schemas, utilities, dependencies

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(
        user: schemas.UserCreate,
        avatar: UploadFile = File(None),  # Add this line for avatar upload
        db: Session = Depends(database.get_db),
        current_user: str = Depends(dependencies.get_current_user_rate_limited),
):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered with this email")

    created_user = crud.create_user(db=db, user=user)

    # Send email verification
    utilities.send_email_verification(created_user.email, created_user.id)

    # Upload avatar to Cloudinary
    if avatar:
        result = upload(avatar.file)
        created_user.avatar_url = result['url']

    response_model = schemas.UserResponse(id=created_user.id, email=created_user.email,
                                          is_active=created_user.is_active)

    return response_model


@router.get("/verify-email/{user_id}", response_model=schemas.Message)
async def verify_email(
        user_id: int,
        db: Session = Depends(database.get_db),
        current_user: str = Depends(dependencies.get_current_user_rate_limited),
):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified")

    crud.update_user_verification_status(db, user_id, True)

    return {"message": "Email successfully verified"}
