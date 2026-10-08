# Unit tests for telemetry_tools.py — run by the `unit-test` CI job.
#
# [PY] `unittest` is Python's built-in test framework (no install needed).
#      JS equivalent:  describe("telemetry_tools", () => { it("...", () => expect(x).toBe(y)) })
#      Python:         class TestX(unittest.TestCase): def test_something(self): self.assertEqual(x, y)
#      Any method starting with `test_` is a test case.
#
# Run locally (from the repo root):
#   python -m unittest discover -s ae-01/sample_project -p "test_*.py" -v
#
# [PY] Docs: https://docs.python.org/3/library/unittest.html

import unittest

from telemetry_tools import average_speed, classify_severity


class TestAverageSpeed(unittest.TestCase):
    def test_average_of_two_records(self):
        records = [{"speed_kmh": 100}, {"speed_kmh": 50}]
        self.assertEqual(average_speed(records), 75)

    def test_empty_records_raises(self):
        # [PY] `with self.assertRaises(...)` ≈ `expect(() => fn()).toThrow()` in Jest
        with self.assertRaises(ValueError):
            average_speed([])


class TestClassifySeverity(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(classify_severity({"engine_temp_c": 99}), "low")
        self.assertEqual(classify_severity({"engine_temp_c": 100}), "medium")
        self.assertEqual(classify_severity({"engine_temp_c": 110}), "high")


if __name__ == "__main__":
    unittest.main()
