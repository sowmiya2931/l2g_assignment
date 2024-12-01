from fastapi import APIRouter, Depends, HTTPException
from utils.auth import decode_token
from utils.database import notes_collection, users_collection
from models import NoteModel

notes_router = APIRouter()

def get_current_user(token: str):
    try:
        payload = decode_token(token)
        user = users_collection.find_one({"user_id": payload["user_id"]})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@notes_router.post("/create")
async def create_note(note_title: str, note_content: str, user: dict = Depends(get_current_user)):
    note = NoteModel(user["user_id"], note_title, note_content)
    notes_collection.insert_one(note.__dict__)
    return {"message": "Note created successfully"}

@notes_router.get("/view")
async def view_notes(user: dict = Depends(get_current_user)):
    notes = list(notes_collection.find({"user_id": user["user_id"]}, {"_id": 0}))
    return notes

@notes_router.put("/update/{note_id}")
async def update_note(note_id: str, note_title: str, note_content: str, user: dict = Depends(get_current_user)):
    result = notes_collection.update_one(
        {"note_id": note_id, "user_id": user["user_id"]},
        {"$set": {"note_title": note_title, "note_content": note_content, "last_update": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note updated successfully"}

@notes_router.delete("/delete/{note_id}")
async def delete_note(note_id: str, user: dict = Depends(get_current_user)):
    result = notes_collection.delete_one({"note_id": note_id, "user_id": user["user_id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
