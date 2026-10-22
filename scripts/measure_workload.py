"""Auditable September 2026 issue workload measurement, including response limitations."""
import json, subprocess, statistics
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
QUERY = """query { search(query:"repo:astral-sh/ruff is:issue created:2026-09-01..2026-09-30",
  type:ISSUE, first:100) {issueCount nodes {... on Issue {
    number title createdAt author{login}
    comments(first:100){nodes{createdAt author{login __typename} authorAssociation}}
    timelineItems(first:100,itemTypes:[LABELED_EVENT]){nodes{
      ... on LabeledEvent{createdAt actor{login __typename} label{name}}}}
  }}}}"""
def run():
    out=subprocess.run(["gh","api","graphql","-f","query="+QUERY],capture_output=True,
                       encoding="utf-8",errors="replace",check=True)
    d=json.loads(out.stdout)["data"]["search"]
    rows=[]
    for issue in d["nodes"]:
        start=datetime.fromisoformat(issue["createdAt"].replace("Z","+00:00"))
        labels=[v for v in issue["timelineItems"]["nodes"]
                if v and v.get("actor") and v["actor"].get("__typename")!="Bot"
                and v["actor"].get("login") not in ("github-actions[bot]",)]
        replies=[v for v in issue["comments"]["nodes"]
                if v.get("author") and v["author"]["__typename"]!="Bot"
                and v["author"]["login"]!=issue["author"]["login"]]
        maint=[v for v in replies if v["authorAssociation"] in
               ("COLLABORATOR","OWNER","MEMBER")]
        def time(a):
            return round((datetime.fromisoformat(min(a,key=lambda x:x["createdAt"])["createdAt"]
                       .replace("Z","+00:00"))-start).total_seconds()/3600,3) if a else None
        rows.append({"id":issue["number"],"created_at":issue["createdAt"],
                     "first_human_label_hours":time(labels),
                     "first_other_human_comment_hours":time(replies),
                     "first_maintainer_comment_hours":time(maint)})
    def stat(k):
        v=[r[k] for r in rows if r[k] is not None]
        return {"count":len(v),"median_hours":statistics.median(v) if v else None,
                "within_24h":sum(x<=24 for x in v)}
    result={"repo":"astral-sh/ruff","window":"2026-09-01..2026-09-30",
            "measurement_date":"2026-10-22",
            "query":'repo:astral-sh/ruff is:issue created:2026-09-01..2026-09-30',
            "total_count":d["issueCount"],
            "first_human_label":stat("first_human_label_hours"),
            "first_other_human_comment":stat("first_other_human_comment_hours"),
            "first_maintainer_comment":stat("first_maintainer_comment_hours"),
            "limits":["Follow-up events measured as of retrieval, not a 30-day fixed follow-up.",
                      "Labels and comments are proxies, not minutes of maintainer labour.",
                      "A label or comment is not proof of correct triage.",
                      "Unreplied issues excluded from conditional medians.",
                      "GitHub authorAssociation can miss maintainers; bot classification based on __typename."],
            "records":sorted(rows,key=lambda x:x["id"])}
    dest=ROOT/"research";dest.mkdir(exist_ok=True)
    (dest/"workload-2026-09.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="records"},indent=2))
if __name__=="__main__":run()
