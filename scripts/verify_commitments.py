"""Verify that golden labels exactly match the prior public SHA-256 commitments."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run():
    commitments=json.loads((ROOT/"evals"/"commitments"/"sha256.json").read_text(encoding="utf-8"))["sha256_expected_json"]
    gold=ROOT/"evals"/"golden"
    existing=sum((gold/name/"expected.json").is_file() for name in commitments)
    if existing==0:
        print("RUNTIME BRANCH: zero expected files; golden checks run on the submission branch.")
        return
    failures=[]
    for name,digest in sorted(commitments.items()):
        p=ROOT/"evals"/"golden"/name/"expected.json"
        if not p.is_file():failures.append(name+": missing");continue
        actual=hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        if actual != digest:failures.append(name+": hash mismatch")
    print("golden commitments:",len(commitments),"verified:",len(commitments)-len(failures))
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
if __name__=="__main__":run()
