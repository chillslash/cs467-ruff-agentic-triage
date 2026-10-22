"""Evaluate evidence completeness and separately grade substantive agent decisions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LABELS={"NONE","CLARIFY","RELATED","ESCALATE"}
def validate():
    inp=ROOT/"evals"/"inputs"
    problems=[]
    rows=[]
    for case in sorted(p for p in inp.iterdir() if p.is_dir()):
        try:
            x=json.loads((case/"input.json").read_text(encoding="utf-8"))
            prior=json.loads((case/"prior_records.json").read_text(encoding="utf-8"))
            for item in prior:
                if item["created_at"]>=x["created_at"]:
                    problems.append(f"{case.name}: future prior item")
            exp=case/"expected.json"
            if exp.exists():
                e=json.loads(exp.read_text(encoding="utf-8"))
                if e["decision"] not in LABELS: problems.append(f"{case.name}: bad decision")
                if not e.get("rationale"): problems.append(f"{case.name}: missing rationale")
                actual=case/"actual.json"
                if actual.exists():
                    a=json.loads(actual.read_text(encoding="utf-8"))
                    predicted=a.get("decision","NO_RUN")
                    rows.append((case.name,e["decision"],predicted,e["decision"]==predicted))
                else: rows.append((case.name,e["decision"],"NO_RUN",False))
        except (OSError,KeyError,ValueError) as err:
            problems.append(f"{case.name}: {err}")
    print("Cases:",len(list(inp.iterdir())))
    print("Case | expected | actual | exact")
    for row in rows: print(" | ".join(map(str,row)))
    if rows:
        completed=[row for row in rows if row[2]!="NO_RUN"]
        print("Executed:",len(completed),"/",len(rows))
        if completed:
            print("Exact action accuracy:",f"{sum(r[3] for r in completed)}/{len(completed)}")
    for problem in problems: print("ERROR:",problem)
    if problems: raise SystemExit(1)
if __name__=="__main__":validate()
