"""Audit live case records against original golden labels and posthoc baseline."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def evaluate():
    data=json.loads((ROOT/"evals"/"results"/"live_runs.json").read_text(encoding="utf-8"))
    cases=data["primary_runs"]
    assert len(cases)==10, "Unexpected live cohort size"
    assert len({c["case_id"] for c in cases})==len(cases),"Duplicate historical case"
    assert len({c["run"] for c in cases})==len(cases),"Duplicate primary run"
    exact=operational=bad_comments=0
    for c in cases:
        p=ROOT/"evals"/"golden"/c["case_id"]/"expected.json"
        gold=json.loads(p.read_text(encoding="utf-8"))
        assert gold["decision"]==c["expected"],c["case_id"]+" frozen expectation changed"
        assert c["observed"] in {"NONE","CLARIFY","RELATED","ESCALATE"}
        assert c["run_url"].endswith(str(c["run"]))
        assert c["source_url"].endswith(str(c["case_id"]))
        intervention=lambda a:a in ("CLARIFY","RELATED")
        assert bool(c["comment"])==intervention(c["observed"]),c["case_id"]+" action/comment mismatch"
        exact+=c["expected"]==c["observed"]
        operational+=intervention(c["expected"])==intervention(c["observed"])
        bad_comments+=bool(c["comment"]) and c["expected"]=="NONE"
    total=sum(c["credits"] for c in cases)
    assert (exact,operational)==(data["aggregate"]["exact"],data["aggregate"]["operational"])
    assert abs(total-data["aggregate"]["total_credits"])<0.000001
    baseline_path=ROOT/"evals"/"results"/"baseline.json"
    baseline=json.loads(baseline_path.read_text(encoding="utf-8"))
    case_ids={c["case_id"] for c in cases}
    subset=[c for c in baseline["cases"] if c["case_id"] in case_ids]
    baseline_exact=sum(bool(c["correct"]) for c in subset)
    print(f"Distinct real cases: {len(cases)}; exact classes {exact}/{len(cases)}; action/no-action {operational}/{len(cases)}")
    print(f"Published comments {sum(bool(c['comment']) for c in cases)}, unnecessary under gold {bad_comments}")
    print(f"Copilot primary AI Credits {total:.6f}; posthoc baseline {baseline_exact}/{len(subset)} exact classes")
if __name__=="__main__":evaluate()
