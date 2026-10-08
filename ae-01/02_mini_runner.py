# Script 02 — Mini GitLab Runner (runs a .gitlab-ci.yml file on your laptop)
#
# You can't use GitLab CI directly, so this script imitates what a GitLab Runner does:
#   1. read the YAML
#   2. work out which jobs belong in this pipeline (rules)
#   3. run stages in order, jobs inside each stage, stop when a stage fails
#   4. print a pipeline summary (like the pipeline graph on a merge request)
#
# Usage (from the repo root, with .venv active):
#   python ae-01/02_mini_runner.py ae-01/01_example.gitlab-ci.yml                              # push to a branch
#   python ae-01/02_mini_runner.py ae-01/01_example.gitlab-ci.yml --source merge_request_event # MR pipeline
#
# Supported keywords: stages, variables, default (image, before_script), stage, script,
#                     before_script, allow_failure, artifacts (paths), rules (if / when: never).
# Not supported (real GitLab has them): needs, include, extends, cache, services, after_script, parallel.
#
# NOTE: like a real runner, this executes the shell commands in YOUR OWN pipeline file.
#       Only run pipeline files you wrote or trust.
#
# [CI] Docs — Predefined variables: https://docs.gitlab.com/ci/variables/predefined_variables/
# [CI] Docs — rules:                https://docs.gitlab.com/ci/jobs/job_rules/

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List

import yaml  # PyYAML (already installed in .venv). Docs: https://pyyaml.org/wiki/PyYAMLDocumentation

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import BLUE, GREEN, RED, RESET, YELLOW  # noqa: E402

RESERVED_KEYS = {"stages", "variables", "default", "include", "workflow", "image",
                 "services", "before_script", "after_script", "cache"}
DEFAULT_STAGES = [".pre", "build", "test", "deploy", ".post"]
SECRET_HINTS = ("TOKEN", "SECRET", "PASSWORD", "KEY")

# Matches one condition like:  $CI_PIPELINE_SOURCE == "push"   or   $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
CONDITION = re.compile(r'^\$(\w+)\s*(==|!=)\s*(?:"([^"]*)"|\$(\w+))$')


def as_list(value) -> List[str]:
    """`script:` can be a single string or a list of strings in YAML."""
    if value is None:
        return []
    return [value] if isinstance(value, str) else list(value)


def as_env(variables) -> Dict[str, str]:
    """YAML variables can be `NAME: value` or `NAME: {value: ..., description: ...}`."""
    return {k: str(v["value"] if isinstance(v, dict) else v) for k, v in (variables or {}).items()}


def condition_matches(expression: str, env: Dict[str, str]) -> bool:
    for part in (p.strip() for p in expression.split("&&")):
        match = CONDITION.match(part)
        if not match:
            raise ValueError(f'Unsupported rule {expression!r}. Use $VAR == "value" or $VAR == $OTHER, joined by &&.')
        name, operator, literal, other_var = match.groups()
        expected = env.get(other_var, "") if other_var else literal
        if (env.get(name, "") == expected) != (operator == "=="):
            return False
    return True


def job_is_included(job: Dict, env: Dict[str, str]) -> bool:
    rules = job.get("rules")
    if not rules:
        return True
    for rule in rules:
        if "if" not in rule or condition_matches(rule["if"], env):
            return rule.get("when", "on_success") != "never"
    return False


def mask_secrets(text: str, env: Dict[str, str]) -> str:
    """Imitates GitLab 'masked' variables: secret values are hidden in job logs."""
    for name, value in env.items():
        if any(hint in name for hint in SECRET_HINTS) and len(value) >= 8:
            text = text.replace(value, "[MASKED]")
    return text


def current_branch() -> str:
    try:
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "main"


def predefined_variables(source: str) -> Dict[str, str]:
    """A few of the variables GitLab sets automatically in every job."""
    branch = current_branch()
    env = {"CI": "true", "CI_PIPELINE_SOURCE": source, "CI_DEFAULT_BRANCH": "main",
           "CI_PROJECT_DIR": str(REPO_ROOT)}
    if source == "merge_request_event":
        # [CI] In MR pipelines GitLab does NOT set CI_COMMIT_BRANCH; it sets the MR branch variables instead.
        env["CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"] = branch
        env["CI_MERGE_REQUEST_TARGET_BRANCH_NAME"] = "main"
    else:
        env["CI_COMMIT_BRANCH"] = branch
    return env


def build_job_env(predefined: Dict[str, str], global_vars: Dict[str, str], job: Dict) -> Dict[str, str]:
    job_vars = as_env(job.get("variables"))
    # Your exported shell variables play the role of GitLab "Settings → CI/CD → Variables",
    # which override variables written in the YAML file.
    settings_overrides = {k: os.environ[k] for k in {**global_vars, **job_vars} if k in os.environ}
    env = {**os.environ, **predefined, **global_vars, **job_vars, **settings_overrides}
    venv_bin = REPO_ROOT / ".venv" / "bin"
    env["PATH"] = f"{venv_bin}{os.pathsep}{env.get('PATH', '')}"
    return env


def run_job(name: str, job: Dict, env: Dict[str, str], default: Dict) -> bool:
    image = job.get("image", default.get("image"))
    print(f"\n{BLUE}━━ Job: {name}  (stage: {job.get('stage', 'test')}){RESET}")
    if image:
        print(f"   GitLab would run this in Docker image '{image}'. Mini runner uses your local .venv.")

    commands = as_list(job.get("before_script", default.get("before_script"))) + as_list(job.get("script"))
    for command in commands:
        print(f"{YELLOW}$ {command}{RESET}")
        result = subprocess.run(command, shell=True, executable="/bin/bash", cwd=REPO_ROOT,
                                env=env, capture_output=True, text=True)
        output = mask_secrets(result.stdout + result.stderr, env)
        if output.strip():
            print(output.rstrip())
        if result.returncode != 0:
            print(f"{RED}✗ Command exited with code {result.returncode}{RESET}")
            return False

    for path in as_list((job.get("artifacts") or {}).get("paths")):
        status = "saved" if (REPO_ROOT / path).exists() else "not found"
        print(f"   artifact {path}: {status}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a .gitlab-ci.yml locally (simplified).")
    parser.add_argument("pipeline_file", type=Path)
    parser.add_argument("--source", default="push", choices=["push", "merge_request_event", "schedule", "web"],
                        help="What triggered the pipeline (sets $CI_PIPELINE_SOURCE)")
    args = parser.parse_args()

    # [PY] yaml.safe_load only builds plain dicts/lists/strings — never use yaml.load on untrusted files.
    config = yaml.safe_load(args.pipeline_file.read_text()) or {}
    stages = config.get("stages", DEFAULT_STAGES)
    default = config.get("default") or {}
    global_vars = as_env(config.get("variables"))
    predefined = predefined_variables(args.source)
    rule_env = {**predefined, **global_vars}

    jobs = {name: job for name, job in config.items() if name not in RESERVED_KEYS and isinstance(job, dict)}
    for name, job in jobs.items():
        if "script" not in job:
            raise SystemExit(f"Job '{name}' has no `script:` — GitLab would reject this file.")
        if job.get("stage", "test") not in stages:
            raise SystemExit(f"Job '{name}' uses stage '{job.get('stage')}' which is not in `stages:` {stages}.")

    included = {name: job for name, job in jobs.items() if job_is_included(job, rule_env)}
    excluded = sorted(set(jobs) - set(included))
    print(f"Pipeline source: {args.source} | branch: {current_branch()} | stages: {' → '.join(stages)}")
    if excluded:
        print(f"Not in this pipeline (rules didn't match): {', '.join(excluded)}")

    summary = []
    pipeline_failed = False
    start = time.time()
    for stage in stages:
        stage_jobs = [(n, j) for n, j in included.items() if j.get("stage", "test") == stage]
        for name, job in stage_jobs:
            if pipeline_failed:
                summary.append((stage, name, "skipped"))
                continue
            env = build_job_env(predefined, global_vars, job)
            passed = run_job(name, job, env, default)
            if passed:
                summary.append((stage, name, "passed"))
            elif job.get("allow_failure"):
                summary.append((stage, name, "failed (allowed)"))
            else:
                summary.append((stage, name, "failed"))
        if any(status == "failed" for s, _, status in summary if s == stage):
            pipeline_failed = True

    colors = {"passed": GREEN, "failed": RED, "failed (allowed)": YELLOW, "skipped": YELLOW}
    print(f"\n{BLUE}━━ Pipeline summary ({time.time() - start:.1f}s){RESET}")
    for stage, name, status in summary:
        print(f"  {stage:<10} {name:<20} {colors[status]}{status}{RESET}")
    print(f"\n{RED}Pipeline FAILED{RESET}" if pipeline_failed else f"\n{GREEN}Pipeline PASSED{RESET}")
    return 1 if pipeline_failed else 0


if __name__ == "__main__":
    sys.exit(main())
