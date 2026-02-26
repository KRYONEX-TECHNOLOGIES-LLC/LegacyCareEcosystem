from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from collections import Counter
import json

router = APIRouter(prefix="/legacy", tags=["Legacy Management"])

class MemoryEntry(BaseModel):
    id: str
    content: str
    media_type: str  # text|audio|video
    timestamp: datetime
    sentiment_score: float
    tags: List[str] = []

class LegacyRequest(BaseModel):
    trigger_type: str  # scheduled|event|manual
    content_filter: List[str] = []

legacy_db = []

@router.post("/capture")
async def capture_memory(entry: MemoryEntry):
    legacy_db.append(entry)
    return {"status": "captured", "memory_id": entry.id}

@router.get("/playback")
async def trigger_legacy_playback(request: LegacyRequest):
    if request.trigger_type == "scheduled":
        # Get most positive memories
        filtered = sorted(legacy_db, 
                        key=lambda x: x.sentiment_score, 
                        reverse=True)[:5]
    else:
        filtered = legacy_db
    
    return {
        "playlist": [
            {
                "id": mem.id,
                "preview": mem.content[:100] + "..." if len(mem.content) > 100 else mem.content,
                "type": mem.media_type
            } for mem in filtered
        ]
    }

@router.get("/summary")
async def generate_legacy_summary():
    if not legacy_db:
        raise HTTPException(status_code=404, detail="No legacy data found")
    
    return {
        "total_memories": len(legacy_db),
        "most_common_tags": Counter([tag for mem in legacy_db for tag in mem.tags]).most_common(3)
    }