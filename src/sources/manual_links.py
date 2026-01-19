from typing import List
from src.models import JobPosting

def load_manual_links(paths: List[str]) -> List[JobPosting]:
    jobs = []

    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = [x.strip() for x in line.split("|")]

                    if len(parts) == 1:
                        # Only URL given
                        url = parts[0]
                        jobs.append(JobPosting(
                            id=url,
                            title="Unknown",
                            company="Unknown",
                            location="",
                            url=url,
                            source="manual"
                        ))
                    else:
                        # Full format: title | company | location | url | source
                        title, company, location, url, source = (parts + ["manual"])[0:5]

                        jobs.append(JobPosting(
                            id=url,
                            title=title,
                            company=company,
                            location=location,
                            url=url,
                            source=source
                        ))
        except FileNotFoundError:
            pass

    return jobs
