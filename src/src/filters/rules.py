from typing import List
from src.models import JobPosting

def score_job(job: JobPosting, cfg: dict) -> float:
    text = ((job.title or "") + " " + (job.description_html or "")).lower()

    kw = cfg["job_preferences"]["keywords"]
    excl = [e.lower() for e in cfg["job_preferences"]["exclude_keywords"]]

    inc_hits = sum(1 for k in kw if k.lower() in text)
    exc_hits = sum(1 for e in excl if e in text)

    score = inc_hits * 2 - exc_hits * 3

    # Location match bonus
    if any(loc.lower() in (job.location or "").lower()
           for loc in cfg["job_preferences"]["locations_include"]):
        score += 1.5

    return max(0.0, round(score, 2))


def shortlist(jobs: List[JobPosting], cfg: dict, min_score: float = 2.0) -> List[JobPosting]:
    out = []
    for j in jobs:
        j.match_score = score_job(j, cfg)
        if j.match_score >= min_score:
            j.status = "shortlisted"
            out.append(j)

    return sorted(out, key=lambda x: x.match_score, reverse=True)
``
