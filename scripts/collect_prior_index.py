"""Capture a bounded pre-September index for deterministic duplicate search.

Only title, date, URL and issue/PR type; no future comments or labels.
The 4-month sampling window is explicit, not an exhaustive search.
"""
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO="astral-sh/ruff"
PERIOD="2026-05-01..2026-08-31"
def query(kind,page):
    q=f"repo:{REPO} is:{kind} created:{PERIOD}"
    p=subprocess.run(["gh","api","-X","GET","search/issues","-f",f"q={q}",
        "-f","per_page=100","-f",f"page={page}"],
        capture_output=True,encoding="utf-8",errors="replace",text=True,check=True)
    return json.loads(p.stdout)
def collect():
    records=[]
    counts={}
    for kind in ("issue","pr"):
        page=1
        while True:
            out=query(kind,page)
            if page==1:counts[kind]=out["total_count"]
            batch=out["items"]
            for item in batch:
                if item["created_at"] >= "2026-09-01":raise ValueError("Post-event record")
                records.append({"number":item["number"],"title":item["title"],
                    "created_at":item["created_at"],"url":item["html_url"],"type":kind})
            print(kind,page,len(batch))
            if len(batch)<100 or page>=9:break
            page+=1
    meta={"project":REPO,"period":PERIOD,"types":counts,
        "collected":len(records),"is_exhaustive_for_period":len(records)==sum(counts.values()),
        "limitations":["Title could be edited after creation; past title revisions unavailable.",
        "No previous issue body, comments, labels or future knowledge stored.",
        "Coverage restricted to May-Aug 2026 and three hand-picked older PRs per case.",
        "GitHub search may have incomplete indexing; metadata used for candidate lookup only."],
        "records":sorted(records,key=lambda x:(x["created_at"],x["number"]))}
    out=ROOT/"reference"/"pre_event_index_2026_05_08.json"
    out.write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("saved",len(records),"of",sum(counts.values()),"complete",meta["is_exhaustive_for_period"])
if __name__=="__main__":collect()

