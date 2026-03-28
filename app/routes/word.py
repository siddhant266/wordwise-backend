from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.huggingface import fetch_word_data

router = APIRouter()


class WordRequest(BaseModel):
    word: str
    book: str


class WordResponse(BaseModel):
    meaning: str
    example: str


@router.post("/lookup", response_model=WordResponse)
async def lookup_word(request: WordRequest):
    word = request.word.strip()
    book = request.book.strip()

    if not word or not book:
        raise HTTPException(status_code=400, detail="Both 'word' and 'book' are required.")

    try:
        result = await fetch_word_data(word, book)
        return WordResponse(
            meaning=result.get("meaning", "Meaning not found."),
            example=result.get("example", "Example not found."),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))