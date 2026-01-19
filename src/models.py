from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobPosting(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    url: str
    source: str
    description_html: Optional[str] = None
    posted_at: Optional[datetime] = None
    match_score: float = 0.0
    status: str = "found"

class ApplicationAssets(BaseModel):
    job_id: str
    resume_variant_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    notes: Optional[str] = None
