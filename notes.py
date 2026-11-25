from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
import database as DB
import auth 
router = APIRouter(prefix="/notes", tags=["Notes"])

class NoteBase(BaseModel):
    content :str

@router.post("/create")
def create_note(note : NoteBase, current_user : dict = Depends(auth.get_current_user)):
    note_id = DB.add_note(current_user["id"], note.content)
    return {"message" : "create note successfully", "id": note_id}

@router.delete("/delete/{note_id}")
def delete_note(note_id : int, current_user : dict = Depends(auth.get_current_user)):
    is_delete = DB.delete_note(note_id, current_user["id"])
    if not is_delete:
        raise HTTPException(status_code=404)
    return {
        "message" : "delete successfully", "user" : {current_user["username"]}, "id" : {current_user["id"]}}

@router.get("/get_all")
def get_all_notes(current_user : dict = Depends(auth.get_current_user)):
    return DB.get_all_notes(current_user["id"])

@router.patch("/edit/{note_id}")
def edit_note(updated_note : NoteBase ,note_id : int, current_user : dict = Depends(auth.get_current_user)):
    updated = DB.update_note(note_id, current_user["id"], updated_note.content)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found or you don't have permission.")
    return {"message" : "edit sucssessfully", "updated" : updated}