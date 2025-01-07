# app/routers/digests.py
from fastapi import APIRouter, HTTPException
from models.Digest import Digest
from database import SessionLocal
from services.text_digests import generate_text_digest

router = APIRouter()

@router.post("/digests/")
async def create_digest(game_id: int):
    db = SessionLocal()
    try:
        # Generate the digest text
        digest_text = await generate_text_digest(game_id)

        # Save the digest to the database
        digest = Digest(game_id=game_id, summary=digest_text)
        db.add(digest)
        db.commit()
        db.refresh(digest)

        return {"message": "Digest created", "digest": digest}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
