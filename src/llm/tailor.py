import os

COVER_LETTER_TEMPLATE = """\
Dear Hiring Manager,

I am applying for the role of {job_title} at {company}. With {years} years of experience in procurement and supply chain, I have driven improvements in SAP S/4HANA and SAP Ariba environments.

Key achievements:
• {a1}
• {a2}
• {a3}

Core skills: {skills}

Regards,
{full_name}
{email} | {phone}
"""

def prepare_cover_letter(job, cfg):
    prof = cfg["profile"]
    ach = prof["achievements"]
    skills = ", ".join(prof["core_skills"][:6])

    text = COVER_LETTER_TEMPLATE.format(
        job_title=job.title,
        company=job.company,
        years=prof["years_experience"],
        a1=ach[0],
        a2=ach[1],
        a3=ach[2],
        skills=skills,
        full_name=prof["full_name"],
        email=prof["email"],
        phone=prof["phone"],
    )
    return text


def save_text(text: str, path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
