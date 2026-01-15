from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud import user_crud

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=dict)
async def create(users:UserCreate):
    user_dict= users.model_dump()
    user_id = await user_crud.create_user(user_dict)
    return {"id": str(user_id)}

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await user_crud.get_user(user_id)
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }

@router.get("/", response_model=list[UserResponse])
async def list_all():
    users = await user_crud.list_users()
    return [
        {
            "id": str(u["_id"]),
            "name": u["name"],
            "email": u["email"],
            "age": u["age"]
        } for u in users
    ]

@router.put("/{user_id}")
async def update_user(user_id: str, user_update: UserUpdate):
    await user_crud.update_user(user_id,user_update.model_dump(exclude_unset=True))
    return {"status":"updated", "message": "User updated successfully"}

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    await user_crud.delete_user(user_id)
    return {"status":"deleted"}