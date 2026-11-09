"""Prepared FastAPI exercise: a small, in-memory notes API."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Our First API")

# Teaching storage only: restarting or reloading the server clears these notes.
notes: list[dict] = []


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes")
def list_notes(q: str | None = None):
    if q is None:
        return notes
    return [note for note in notes if q.lower() in note["title"].lower()]


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    saved_note = {"id": len(notes) + 1, **note.model_dump()}
    notes.append(saved_note)
    return saved_note
