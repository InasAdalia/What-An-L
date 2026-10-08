# Eval gate — run by the `eval-gate` CI job.
#
# Unit tests check "does the code behave as written?".
# An eval checks "is the output GOOD ENOUGH on realistic cases?" and returns a SCORE.
# The gate fails the pipeline (exit code 1) if the score is below a threshold.
#
# Here the "model" is a plain function so it runs anywhere with no LLM.
# In AE-08 the same idea is used with a real agent + an LLM judge (Eval Agent) + MLflow.
#
# [CI] GitLab decides pass/fail ONLY from the exit code: 0 = pass, anything else = fail.
#      [PY] sys.exit(1) ≈ process.exit(1) in Node.

import json
import os
import sys
from pathlib import Path

from telemetry_tools import classify_severity

# A "golden dataset": inputs + the answer we expect. Real projects keep this in a file/table.
GOLDEN_SET = [
    {"record": {"car_id": "C-01", "engine_temp_c": 85}, "expected": "low"},
    {"record": {"car_id": "C-02", "engine_temp_c": 99}, "expected": "low"},
    {"record": {"car_id": "C-03", "engine_temp_c": 100}, "expected": "medium"},
    {"record": {"car_id": "C-04", "engine_temp_c": 104}, "expected": "medium"},
    {"record": {"car_id": "C-05", "engine_temp_c": 109}, "expected": "medium"},
    {"record": {"car_id": "C-06", "engine_temp_c": 110}, "expected": "high"},
    {"record": {"car_id": "C-07", "engine_temp_c": 118}, "expected": "high"},
    {"record": {"car_id": "C-08", "engine_temp_c": 125}, "expected": "high"},
    {"record": {"car_id": "C-09", "engine_temp_c": 72}, "expected": "low"},
    {"record": {"car_id": "C-10", "engine_temp_c": 101}, "expected": "medium"},
]

REPORT_PATH = Path(__file__).resolve().parent / "eval_report.json"


def main() -> int:
    # [CI] The threshold comes from a CI variable, so you can tune it without changing code.
    threshold = float(os.environ.get("EVAL_THRESHOLD", "0.8"))

    results = []
    for case in GOLDEN_SET:
        actual = classify_severity(case["record"])
        results.append({
            "car_id": case["record"]["car_id"],
            "expected": case["expected"],
            "actual": actual,
            "passed": actual == case["expected"],
        })

    score = sum(r["passed"] for r in results) / len(results)

    # [CI] This file is saved as an "artifact" so reviewers can download it from the MR page.
    REPORT_PATH.write_text(json.dumps({"score": score, "threshold": threshold, "results": results}, indent=2))

    print(f"Eval score: {score:.2f} (threshold {threshold:.2f})")
    for r in results:
        if not r["passed"]:
            print(f"  FAILED {r['car_id']}: expected {r['expected']}, got {r['actual']}")

    return 0 if score >= threshold else 1


if __name__ == "__main__":
    sys.exit(main())
