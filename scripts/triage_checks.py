"""Deterministic parsing/search over pre-decision snapshots; never a classifier."""
from pathlib import Path
import argparse, json, re, math
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
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--case",required=True)
    args=parser.parse_args()
    print(json.dumps(inspect_case(args.case),indent=2,ensure_ascii=False))
