"""Collect pre-decision issue snapshots. Execute only for the fixed, reviewed cohort.

Requires authenticated GitHub CLI; never include post-event comments or labels.
Re-running must not silently overwrite curated input fixtures.
"""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IDS = [28220, 28274, 28308, 28340, 28483, 28493, 28503, 28602,
       28618, 28661, 28721, 28732, 28777, 28842, 28893, 28942, 28989]
PREDECESSORS = {28503: [26584], 28989: [16149], 28893: [26113]}
def gh(path):
    proc = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return json.loads(proc.stdout)
def graph(query):
    proc = subprocess.run(["gh","api","graphql","-f",f"query={query}"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return json.loads(proc.stdout)["data"]
def collect(force=False):
    targets = ROOT/"evals"/"inputs"
    targets.mkdir(parents=True, exist_ok=True)
    policy_sha = gh("/repos/astral-sh/ruff/commits?path=CONTRIBUTING.md&until=2026-08-31T23%3A59%3A59Z&per_page=1")[0]["sha"]
    (ROOT/"reference").mkdir(exist_ok=True)
    refmeta = {"repository":"astral-sh/ruff", "policy_commit":policy_sha,
               "cutoff":"2026-08-31T23:59:59Z","source":"GitHub API"}
    (ROOT/"reference"/"source.json").write_text(json.dumps(refmeta,indent=2)+"\n",encoding="utf-8")
    for source, destination in [
        ("CONTRIBUTING.md","CONTRIBUTING.md"),
        (".github/ISSUE_TEMPLATE/1_bug_report.yaml","bug_report.yaml"),
        (".github/ISSUE_TEMPLATE/2_rule_request.yaml","rule_request.yaml"),
        (".github/ISSUE_TEMPLATE/3_question.yaml","question.yaml")
    ]:
        contents = gh(f"/repos/astral-sh/ruff/contents/{source}?ref={policy_sha}")
        import base64
        text = base64.b64decode(contents["content"]).decode("utf-8")
        path=ROOT/"reference"/destination
        if not path.exists() or force:
            path.write_text(text,encoding="utf-8")
    for n in IDS:
        dest=targets/str(n)
        if (dest/"input.json").exists() and not force:
            print(n,"preserved")
            continue
        issue=gh(f"/repos/astral-sh/ruff/issues/{n}")
        data=graph(f'query{{repository(owner:"astral-sh",name:"ruff"){{issue(number:{n}){{createdAt lastEditedAt}}}}}}')
        edit=data["repository"]["issue"]["lastEditedAt"]
        if edit is not None:
            raise RuntimeError(f"Refuse edited issue #{n}, edited {edit}")
        if "pull_request" in issue:
            raise RuntimeError("not an issue")
        dest.mkdir(parents=True,exist_ok=True)
        record={"source_repository":"astral-sh/ruff","source_number":n,
                "source_url":issue["html_url"],"created_at":issue["created_at"],
                "title":issue["title"],"body":issue["body"],
                "snapshot_basis":"Issue body unchanged according to GraphQL lastEditedAt; comments and labels intentionally excluded",
                "collected_at":datetime.now(timezone.utc).isoformat()}
        (dest/"input.json").write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        priors=[]
        for ref in PREDECESSORS.get(n,[]):
            r=gh(f"/repos/astral-sh/ruff/issues/{ref}")
            if r["created_at"] >= issue["created_at"]:
                raise RuntimeError(f"future reference {ref} for {n}")
            priors.append({"number":ref,"title":r["title"],"url":r["html_url"],
                           "created_at":r["created_at"],"type":"PR" if "pull_request" in r else "issue",
                           "note":"Only title and date are exposed; current body/comments/labels omitted"})
        (dest/"prior_records.json").write_text(json.dumps(priors,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print(n,"captured",len(priors),"earlier records")
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--force",action="store_true")
    collect(**vars(p.parse_args()))
