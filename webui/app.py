import os, subprocess
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template

app = FastAPI()

# HTML interface
INDEX_TMPL = Template("""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Job Apply Agent</title>
  <style>
    body { font-family: Arial; margin: 32px; }
    textarea { width:100%; height:180px; }
    .card { border:1px solid #ddd; padding:20px; border-radius:8px; margin-bottom:25px; }
    button { padding:10px 18px; }
    pre { background:#f7f7f7; padding:12px; border-radius:6px; }
  </style>
</head>
<body>
  <h2>Job Apply Agent (Semi‑Auto Mode)</h2>

  <div class="card">
    <h3>1) Paste Job URLs</h3>
    /add
      <textarea name="urls" placeholder="Paste job URLs (1 per line)..."></textarea>
      <br><br>
      <button type="submit">Save URLs</button>
    </form>
  </div>

  <div class="card">
    <h3>2) Prepare Applications</h3>
    /prepare
      <button type="submit">Prepare Now</button>
    </form>
    <small>This will generate cover letters and shortlist results.</small>
  </div>

  <div class="card">
    <h3>3) Results</h3>
    <pre>{{ report }}</pre>
  </div>

</body>
</html>
""")

def init_source_files():
    os.makedirs("config/sources", exist_ok=True)
    for name in ["linkedIn","naukri","indeed","foundit",
                 "hirect","shine","instahyre","cutshort","company_portals"]:
        path = f"config/sources/{name}.txt"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("# Paste URLs here\n")

@app.get("/", response_class=HTMLResponse)
def home():
    init_source_files()
    report_path = "data/outputs/shortlist_report.txt"
    report = ""
    if os.path.exists(report_path):
        report = open(report_path).read()
    return INDEX_TMPL.render(report=report)

@app.post("/add")
def add(urls: str = Form(...)):
    init_source_files()
    inbox = "config/sources/company_portals.txt"
    with open(inbox, "a", encoding="utf-8") as f:
        for line in urls.splitlines():
            line=line.strip()
            if line:
                f.write(line + "\n")
    return RedirectResponse("/", status_code=303)

@app.post("/prepare")
def prepare():
    subprocess.run(["python", "src/orchestrator.py"], check=False)
    return RedirectResponse("/", status_code=303)

@app.get("/health")
def health():
    return {"status": "ok"}
