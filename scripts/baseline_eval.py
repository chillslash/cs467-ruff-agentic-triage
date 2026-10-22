"""Simple conventional-automation comparator, not an independent gold-label study.

The heuristic was designed after seeing the corpus, so it must NOT be described
as a pre-registered or held-out baseline. It illustrates tradeoffs only.
"""
import json,re
from pathlib import Path
from triage_checks import inspect_case
ROOT=Path(__file__).resolve().parents[1]
RULE_REQUEST=re.compile(r"(?:^|\\b)(?:add|support|proposal|new rule|feature|option|allow|warn if|should|change request|config option|emit error|request)(?:\\b|$)",re.I)
def decide(case):
    src=ROOT/"evals"/"inputs"/case
    row=json.loads((src/"input.json").read_text(encoding="utf-8"))
    title=row.get("title","")
    body=row.get("body","") or ""
    cues=inspect_case(case)
    r=cues["rubric_cues"]
    if r["mentions_pylint"]:return "CLARIFY","Explicit third-party tooling reference"
    if RULE_REQUEST.search(title):return "ESCALATE","Likely change or rule request by title"
    if any(p["type"].lower()=="pr" and p["score"]>=9 and p["shared_rule_ids"] for p in cues["prior_candidates"]):
        return "RELATED","Rule-ID matching earlier PR title"
    if not r["contains_code_or_reproduction"] and not r["mentions_ruff_command"]:
        return "CLARIFY","No command or code-like reproduction"
    return "NONE","Sufficient field cues / no matching rule"
def run():
    actual=[]
    for p in sorted((ROOT/"evals"/"inputs").glob("*/input.json")):
        cid=p.parent.name
        gold=ROOT/"evals"/"golden"/cid/"expected.json"
        if not gold.exists():continue
        e=json.loads(gold.read_text(encoding="utf-8"))
        pred,why=decide(cid)
        actual.append({"case_id":cid,"expected":e["decision"],"predicted":pred,"correct":pred==e["decision"],"explanation":why,"synthetic":bool(e.get("synthetic"))})
    if not actual:
        print("No gold labels on this branch; see the submission branch")
        return
    correct=sum(x["correct"] for x in actual)
    false_interventions=sum(x["expected"] not in ("CLARIFY","RELATED") and x["predicted"] in ("CLARIFY","RELATED") for x in actual)
    out={"baseline":"posthoc conventional heuristics (not preregistered)", "n":len(actual),
          "exact":correct,"false_interventions":false_interventions,"cases":actual}
    target=ROOT/"evals"/"results"/"baseline.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(f"Baseline exact {correct}/{len(actual)}; unnecessary intervention attempts {false_interventions}")
    for x in actual:
        if not x["correct"]:print(x["case_id"],x["expected"],"->",x["predicted"])
if __name__=="__main__":run()

