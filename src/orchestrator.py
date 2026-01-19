import os, yaml
from datetime import datetime
from typing import List
from src.models import JobPosting, ApplicationAssets
from src.filters.rules import shortlist
from src.llm.tailor import prepare_cover_letter, save_text
from src.sources.manual_links import load_manual_links

def load_cfg():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dirs(cfg):
    os.makedirs(cfg["storage"]["output_dir"], exist_ok=True)
    os.makedirs("data/logs", exist_ok=True)

def prepare_assets(job: JobPosting, cfg: dict) -> ApplicationAssets:
    out_dir = os.path.join(cfg["storage"]["output_dir"], job.id.replace("/", "_")[:150])
    os.makedirs(out_dir, exist_ok=True)

    # Generate cover letter
    cl_text = prepare_cover_letter(job, cfg)
    cl_path = save_text(cl_text, os.path.join(out_dir, "cover_letter.txt"))

    # Resume variant (we use a single master resume stored in data/outputs/)
    resume_path = "data/outputs/master_resume.pdf"
    if not os.path.exists(resume_path):
        # Create a placeholder if user hasn't uploaded their real resume yet
        save_text("Upload your resume as master_resume.pdf", "data/outputs/PLEASE_UPLOAD_RESUME.txt")

    return ApplicationAssets(job_id=job.id, resume_variant_path=resume_path, cover_letter_path=cl_path)

def collect_jobs(cfg) -> List[JobPosting]:
    jobs = []
    # Read pasted links from all portals
    manual_files = [
        "config/sources/linkedIn.txt",
        "config/sources/naukri.txt",
        "config/sources/indeed.txt",
        "config/sources/foundit.txt",
        "config/sources/hirect.txt",
        "config/sources/shine.txt",
        "config/sources/instahyre.txt",
        "config/sources/cutshort.txt",
        "config/sources/company_portals.txt",
    ]
    jobs += load_manual_links(manual_files)

    # Remove duplicates by URL
    unique = {}
    for j in jobs:
        unique[j.id] = j
    return list(unique.values())

def main():
    cfg = load_cfg()
    ensure_dirs(cfg)

    jobs = collect_jobs(cfg)
    shortlisted = shortlist(jobs, cfg)

    print(f"Found {len(jobs)} jobs; Shortlisted {len(shortlisted)}")

    prepared = []
    for j in shortlisted:
        assets = prepare_assets(j, cfg)
        j.status = "prepared"
        prepared.append((j, assets))

    # Save a simple shortlist report for the web UI to display
    report_path = "data/outputs/shortlist_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        for j, assets in prepared:
            f.write(f"[{j.match_score:.1f}] {j.title} @ {j.company} | {j.location}\n{j.url}\nCover letter: {assets.cover_letter_path}\nResume: {assets.resume_variant_path}\n\n")

    print(f"Shortlist saved to {report_path}")

if __name__ == "__main__":
    main()
