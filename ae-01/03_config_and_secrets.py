# Script 03 — Config & secrets the enterprise way
#
# Rule: code reads secrets from ENVIRONMENT VARIABLES. Where those come from depends on where it runs:
#   laptop      → `export NAME=...` in your terminal (or a git-ignored .env file)
#   GitLab CI   → Settings → CI/CD → Variables (masked + protected)
#   Databricks  → Databricks secret scopes, or the agent's service principal identity
# The code stays the SAME in all three places. Only the environment changes.
#
# Try it (from the repo root):
#   python ae-01/03_config_and_secrets.py                    # fails fast: missing variables
#   export DATABRICKS_HOST="https://fake-workspace.example.com"
#   export DATABRICKS_TOKEN="FAKE-TOKEN-FOR-TESTING-123456"
#   python ae-01/03_config_and_secrets.py                    # works, token is masked
#
# [CI] Docs — CI/CD variables: https://docs.gitlab.com/ci/variables/
# [DB] Docs — Databricks secrets: https://docs.databricks.com/aws/en/security/secrets/

import os
import sys

# ✗ NEVER do this — the token ends up in git history forever, even if you delete it later:
#   DATABRICKS_TOKEN = "dapi1234..."
#
# ✓ Read it from the environment.
# [PY] os.environ.get("X")  ≈  process.env.X  in Node.  Returns None if missing (JS: undefined).

REQUIRED_VARS = ["DATABRICKS_HOST", "DATABRICKS_TOKEN"]

# Non-secret config can have safe defaults.
MODEL_NAME = os.environ.get("MODEL_NAME", "llama3.2:3b")


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        # Fail fast with a helpful message. Note: the message names the variable, never a value.
        sys.exit(f"Missing environment variable {name}. "
                 f"Locally: export {name}=...   In GitLab: Settings → CI/CD → Variables")
    return value


def mask(value: str) -> str:
    """Show just enough to recognise which token it is, never the full value."""
    return value[:4] + "****" if len(value) > 8 else "****"


if __name__ == "__main__":
    # [PY] Dict comprehension ≈ Object.fromEntries(REQUIRED_VARS.map(n => [n, getRequiredEnv(n)]))
    config = {name: get_required_env(name) for name in REQUIRED_VARS}

    print(f"Model:       {MODEL_NAME}")
    print(f"Workspace:   {config['DATABRICKS_HOST']}")
    print(f"Token:       {mask(config['DATABRICKS_TOKEN'])}")
    # In a real project this is where you'd create the client, e.g.
    #   from databricks.sdk import WorkspaceClient
    #   client = WorkspaceClient()   # the SDK reads DATABRICKS_HOST / DATABRICKS_TOKEN from env by itself
