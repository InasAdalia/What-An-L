# Sample project — the "code under test" for the AE-01 pipeline.
# In a real agent project these would be the tools your agent calls (LC Day 9–10).
# The pipeline in 01_example.gitlab-ci.yml lints, tests and evaluates this file.
#
# [PY] Python 3.9: use `List[Dict]` from typing (like `Array<Record<string, any>>` in TS).
#      `list[dict]` also works on 3.9, but `X | Y` union types need 3.10+.

from typing import Dict, List


def average_speed(records: List[Dict]) -> float:
    """Average `speed_kmh` across telemetry records."""
    if not records:
        raise ValueError("records must not be empty")
    return sum(r["speed_kmh"] for r in records) / len(records)


def classify_severity(record: Dict) -> str:
    """Classify engine temperature into low / medium / high severity."""
    temp = record["engine_temp_c"]
    if temp >= 110:
        return "high"
    if temp >= 100:
        return "medium"
    return "low"
