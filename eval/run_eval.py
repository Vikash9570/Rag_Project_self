"""Baseline eval for a RAG /ask endpoint.

Usage:
  python eval/run_eval.py --dry-run
  python eval/run_eval.py --url http://localhost:8000/ask --k 5 --page-offset 0

Metrics (the three baseline numbers):
  retrieval_hit_rate : answerable questions where a retrieved chunk's page is in gold_pages
  keyword_match      : mean fraction of expected_keywords found in the answer (answerable only)
  refusal_rate       : unanswerable questions the system correctly refuses
Also reported: false_refusal_rate (answerable questions it wrongly refuses).

Adapt extract() to your /ask response shape. Default assumption:
  {"answer": "...", "sources": [{"page": 3, "text": "..."}, ...]}
--page-offset is added to the stored page to get a 1-based PDF page
(use 1 if your loader stores 0-based page numbers).
"""
import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

REFUSAL_RE = re.compile(
    r"(don't|do not|doesn't|does not) (know|contain|have|say|mention|provide)"
    r"|not (mentioned|provided|found|stated|specified|covered|available)"
    r"|no (information|mention|details?)"
    r"|(cannot|can't|couldn't|could not|unable to) (find|answer|determine)"
    r"|(isn't|is not|aren't|are not) (mentioned|covered|in the)"
    r"|not in the (document|context|provided)"
    r"|outside (the )?(scope|document)",
    re.I,
)


def load_eval(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def ask(url, question, k, timeout):
    body = json.dumps({"question": question, "top_k": k}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def extract(resp, cited_id):
    """Return (answer_text, set_of_retrieved_pages_1_based). EDIT to match your API."""
    answer = resp.get("answer", "")
    pages = set()
    for s in resp.get("sources", []) or []:
        p = s.get("page")
        if p is None:
            p = (s.get("metadata") or {}).get("page")
        if p is not None:
            pages.add(int(p) + cited_id)
    return answer, pages


def keyword_score(answer, kws):
    if not kws:
        return None
    a = answer.lower()
    return sum(1 for k in kws if k.lower() in a) / len(kws)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def summarize(rows):
    ans = [r for r in rows if r["answerable"]]
    una = [r for r in rows if not r["answerable"]]
    return {
        "n_answerable": len(ans),
        "n_unanswerable": len(una),
        "retrieval_hit_rate": mean([1.0 if r["hit"] else 0.0 for r in ans]),
        "keyword_match": mean([r["kw"] for r in ans]),
        "refusal_rate": mean([1.0 if r["refused"] else 0.0 for r in una]),
        "false_refusal_rate": mean([1.0 if r["refused"] else 0.0 for r in ans]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default=str(Path(__file__).with_name("eval_set.jsonl")))
    ap.add_argument("--url", default="http://localhost:8000/ask")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--page-offset", type=int, default=0)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--out", default="eval/results/baseline.json")
    ap.add_argument("--dry-run", action="store_true", help="validate the eval set only")
    args = ap.parse_args()

    items = load_eval(args.eval)
    if args.dry_run:
        by = {}
        for it in items:
            by[it["type"]] = by.get(it["type"], 0) + 1
        print(f"{len(items)} questions: {by}")
        return

    results = []
    for it in items:
        t0 = time.time()
        try:
            resp = ask(args.url, it["question"], args.k, args.timeout)
            answer, pages = extract(resp, args.page_offset)
            err = None
        except Exception as e:  # keep going; count as miss
            answer, pages, err = "", set(), str(e)
        refused = bool(REFUSAL_RE.search(answer))
        hit = bool(pages & set(it["gold_pages"])) if it["answerable"] else None
        results.append({
            "id": it["id"], "type": it["type"], "answerable": it["answerable"],
            "tags": it["tags"], "hit": hit,
            "kw": keyword_score(answer, it["expected_keywords"]) if it["answerable"] else None,
            "refused": refused, "retrieved_pages": sorted(pages),
            "gold_pages": it["gold_pages"], "answer": answer,
            "latency_s": round(time.time() - t0, 2), "error": err,
        })
        print(f"{it['id']}: hit={hit} refused={refused} pages={sorted(pages)} err={err}")

    overall = summarize(results)
    no_diagram = summarize([r for r in results if "diagram_only" not in r["tags"]])
    report = {"k": args.k, "overall": overall, "excluding_diagram_only": no_diagram, "rows": results}

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n=== BASELINE (k=%d) ===" % args.k)
    for name, s in (("overall", overall), ("excluding diagram_only", no_diagram)):
        print(f"[{name}]  answerable={s['n_answerable']}  unanswerable={s['n_unanswerable']}")
        print(f"  retrieval hit rate : {s['retrieval_hit_rate']:.1%}")
        print(f"  keyword match      : {s['keyword_match']:.1%}")
        print(f"  refusal rate       : {s['refusal_rate']:.1%}  (unanswerable correctly refused)")
        print(f"  false refusal rate : {s['false_refusal_rate']:.1%}  (answerable wrongly refused)")
    print(f"\nSaved per-question results to {out}")


if __name__ == "__main__":
    main()
