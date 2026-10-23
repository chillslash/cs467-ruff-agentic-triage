"""Deterministic parsing/search over pre-decision snapshots; never a classifier."""
from pathlib import Path
import argparse, json, re, math, os, urllib.request
ROOT=Path(__file__).resolve().parents[1]
RULE=re.compile(r"\b(?:[A-Z]{1,5}\d{3,4}|RUF\d{3}|PLR\d{4})\b")
COMMAND=re.compile(r"(?im)^\s*(?:\$\s*)?(?:uvx\s+)?ruff\s+(?:check|format|analyze|version)\b")
VERSION=re.compile(r"(?i)\b(?:ruff\s*(?:v|version)?\s*\d+\.\d+(?:\.\d+)?|version\s*[:=]?\s*\d+\.\d+)")
CODE=re.compile(r"(?m)```|^\s*(?:def |class |from |import |\$ ruff|ruff check|ruff format)")
def tokens(text):
    stop={"the","for","and","when","with","from","does","not","are","this","that","into","some","which","ruff","rule","issue","python"}
    return {w for w in re.findall(r"[a-z0-9]{3,}",text.lower()) if w not in stop}
def inspect_case(case, base=ROOT):
    identifier=str(case)
    if not re.fullmatch(r"\d{4,7}|adv-[a-z-]+",identifier):
        raise ValueError("Invalid case id")
    src=base/"evals"/"inputs"/identifier
    x=json.loads((src/"input.json").read_text(encoding="utf-8"))
    priors=json.loads((src/"prior_records.json").read_text(encoding="utf-8"))
    text=x["title"]+"\n"+(x.get("body") or "")
    cutoff=x["created_at"]
    # An intentionally bounded, pre-event title-only search index.
    index_file=base/"reference"/"pre_event_index_2026_05_08.json"
    if index_file.exists():
        index=json.loads(index_file.read_text(encoding="utf-8"))
        priors+=index["records"]
    matches=[]
    for p in priors:
        if p["created_at"] >= cutoff:
            raise ValueError("Future-information leakage in prior records")
        shared=tokens(text)&tokens(p["title"])
        prior_rules=set(RULE.findall(p["title"]))
        shared_rules=set(RULE.findall(text))&prior_rules
        score=len(shared)+5*len(shared_rules)
        if score>=2 or shared_rules:
            matches.append({**p,"shared_term_count":len(shared),
                            "shared_rule_ids":sorted(shared_rules),"score":score})
    matches.sort(key=lambda m:(-m["score"],-m["shared_term_count"],m["number"]))
    # Deduplicate curated predecessors and indexed records by number.
    unique=[]
    visited=set()
    for item in matches:
        if item["number"] not in visited:
            unique.append(item)
            visited.add(item["number"])
    return {"source_id":identifier,"source_time":cutoff,
        "prior_index_limitations":"Title-only May-Aug 2026 index and curated earlier PRs; may miss duplicates. Results are suggestions, not decisions.",
        "indexed_candidates_total":len(unique),
        "rubric_cues":{"rule_ids":sorted(set(RULE.findall(text))),
          "mentions_version":bool(VERSION.search(text)),
          "mentions_ruff_command":bool(COMMAND.search(text)),
          "contains_code_or_reproduction":bool(CODE.search(text)),
          "mentions_pylint":bool(re.search(r"\bpylint\b",text,re.I)),
          "links":len(re.findall(r"https?://",text))},
        "prior_candidates":unique[:12],
        "caveat":"Field cues are not decisions; assess applicability and sufficiency yourself."}

# Sandbox issue #N and historical Ruff issue #ID are distinct.
TRIGGER = re.compile(r"^\[EVAL\] #(?P<source>\d{4,7}|adv-[a-z-]+): (?P<title>.+)$")
SANDBOX = "chillslash/cs467-ruff-agentic-triage"

def inspect_trigger(issue_number, base=ROOT, issue_payload=None, event_file=None):
    number = int(issue_number)
    if not (1 <= number <= 9999999):
        raise ValueError("Invalid sandbox issue number")
    if issue_payload is None:
        event_path = event_file or os.environ.get("GITHUB_EVENT_PATH")
        if event_path:
            if not Path(event_path).is_file():
                raise ValueError("GitHub event file is missing")
            event = json.loads(Path(event_path).read_text(encoding="utf-8"))
            if event.get("repository", {}).get("full_name") != SANDBOX:
                raise ValueError("Unexpected triggering repository")
            if event.get("action") != "opened":
                raise ValueError("Not an opened-issue event")
            issue_payload = event.get("issue")
        if issue_payload is None:
            request = urllib.request.Request(
                f"https://api.github.com/repos/{SANDBOX}/issues/{number}",
                headers={"Accept": "application/vnd.github+json", "User-Agent": "CS467-Ruff-evaluation"})
            with urllib.request.urlopen(request, timeout=12) as response:
                issue_payload = json.load(response)
    if not isinstance(issue_payload, dict) or issue_payload.get("number") != number:
        raise ValueError("Trigger issue number mismatch")
    match = TRIGGER.fullmatch(issue_payload.get("title") or "")
    if not match:
        raise ValueError("Invalid or missing [EVAL] source ID")
    source_id = match.group("source")
    path = base / "evals" / "inputs" / source_id / "input.json"
    if not path.is_file():
        raise ValueError("Unknown frozen source ID")
    source = json.loads(path.read_text(encoding="utf-8"))
    if match.group("title") != source["title"]:
        raise ValueError("Source title does not match frozen historical fixture")
    expected = (f"Historical or synthetic sandbox evaluation case {source_id}; "
                f"SOURCE: {source.get('source_url') or 'synthetic'}\n\n"
                f"{source.get('body') or ''}")
    normalise = lambda value: (value or "").replace("\r\n", "\n").strip()
    if normalise(issue_payload.get("body")) != normalise(expected):
        raise ValueError("Trigger body does not match frozen historical fixture")
    result = inspect_case(source_id, base)
    result["sandbox_issue_number"] = number
    result["binding_validated"] = True
    # A single verified report means the model need not guess fixture paths.
    # Only the original source body is exposed, never post-event outcomes.
    result["verified_issue"] = {
        "source_id": source_id, "title": source["title"],
        "body": source.get("body") or "", "source_url": source.get("source_url"),
        "created_at": source["created_at"],
    }
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    target=parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--case",help="Offline fixture check only")
    target.add_argument("--issue-number",type=int,help="Resolve triggering sandbox issue to verified historical source")
    parser.add_argument("--event-file",help="Read the trusted event payload from the Actions runner before AI execution")
    args=parser.parse_args()
    result=inspect_trigger(args.issue_number,event_file=args.event_file) if args.issue_number else inspect_case(args.case)
    print(json.dumps(result,indent=2,ensure_ascii=True))
