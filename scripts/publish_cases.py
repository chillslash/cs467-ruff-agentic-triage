"""Publish a frozen case to this sandbox only; does not touch upstream."""
import argparse,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO="chillslash/cs467-ruff-agentic-triage"
def publish(case):
    if not re.fullmatch(r"\d{4,7}|adv-[a-z-]+",case): raise ValueError(case)
    path=ROOT/"evals"/"inputs"/case/"input.json"
    x=json.loads(path.read_text(encoding="utf-8"))
    title=f"[EVAL] #{case}: {x['title']}"
    body=f"Historical or synthetic sandbox evaluation case {case}; SOURCE: {x['source_url'] or 'synthetic'}\n\n"+(x["body"] or "")
    bodyfile=ROOT/".temp"/f"{case}-body.md";bodyfile.parent.mkdir(exist_ok=True)
    bodyfile.write_text(body,encoding="utf-8")
    try:
        result=subprocess.run(["gh","issue","create","-R",REPO,"--title",title,"--body-file",str(bodyfile)],
            capture_output=True,text=True,encoding="utf-8",errors="replace",check=True)
    finally: bodyfile.unlink(missing_ok=True)
    url=result.stdout.strip()
    dest=ROOT/"evals"/"results";dest.mkdir(parents=True,exist_ok=True)
    tracker=dest/"issue_map.json"
    data=json.loads(tracker.read_text(encoding="utf-8")) if tracker.exists() else {}
    data[case]=url
    tracker.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(url)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--case",required=True)
    publish(p.parse_args().case)
