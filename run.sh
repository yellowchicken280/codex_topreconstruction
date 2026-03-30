#!/usr/bin/env bash
# run.sh — launch codexlikeagent for topreco tasks
#
# Usage:
#   ./run.sh prompts/01_orchestrate.txt              # run a preset prompt
#   ./run.sh prompts/01_orchestrate.txt my-session   # with named session (enables memory across runs)
#   ./run.sh "your prompt text here"                 # inline prompt
#
# Environment (add to ~/.bashrc):
#   export OPENAI_BASE_URL="https://api.cborg.lbl.gov"
#   export CBORG_API_KEY="your-key-here"
#   export OPENAI_API_KEY="$CBORG_API_KEY"

set -euo pipefail

AGENT_DIR=/global/u1/v/vinny/projects/codexlikeagent
SELF_DIR=/global/u1/v/vinny/projects/topreco-agent
CONFIG=$SELF_DIR/config.yaml
CBORG_ENV="$AGENT_DIR/agent_kit/cborg_env.sh"

PROMPT_OR_FILE="${1:-}"
SESSION="${2:-}"

if [[ -z "$PROMPT_OR_FILE" ]]; then
  echo "Usage: $0 <prompt-file-or-text> [session-name]"
  exit 1
fi

# Auto-source cborg_env.sh if env vars aren't already set
if [[ -z "${OPENAI_BASE_URL:-}" ]] && [[ -f "$CBORG_ENV" ]]; then
  # shellcheck disable=SC1090
  source "$CBORG_ENV"
fi

# Mirror CBORG_API_KEY -> OPENAI_API_KEY if needed
if [[ -n "${CBORG_API_KEY:-}" ]] && [[ -z "${OPENAI_API_KEY:-}" ]]; then
  export OPENAI_API_KEY="$CBORG_API_KEY"
fi

if [[ -z "${OPENAI_BASE_URL:-}" ]]; then
  echo "Error: OPENAI_BASE_URL is not set."
  echo "  Add to ~/.bashrc:"
  echo "    export OPENAI_BASE_URL=\"https://api.cborg.lbl.gov\""
  echo "    export CBORG_API_KEY=\"your-key-here\""
  echo "    export OPENAI_API_KEY=\"\$CBORG_API_KEY\""
  exit 1
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Error: OPENAI_API_KEY (or CBORG_API_KEY) is not set."
  echo "  Get your key from the CBorg portal and add to ~/.bashrc:"
  echo "    export CBORG_API_KEY=\"your-key-here\""
  echo "    export OPENAI_API_KEY=\"\$CBORG_API_KEY\""
  exit 1
fi

# Build agent args — workspace is this directory (prompts live here; keeps large parquet out)
AGENT_ARGS=(
  --config "$CONFIG"
  --workspace "$SELF_DIR"
)

# Prompt: file or inline string
# Resolve relative paths against SELF_DIR so agent can verify they're inside the workspace
if [[ -f "$PROMPT_OR_FILE" ]]; then
  ABS_PROMPT="$(cd "$(dirname "$PROMPT_OR_FILE")" && pwd)/$(basename "$PROMPT_OR_FILE")"
  AGENT_ARGS+=(--request-file "$ABS_PROMPT")
else
  AGENT_ARGS+=(--prompt "$PROMPT_OR_FILE")
fi

# Session: enable memory across runs when provided
if [[ -n "$SESSION" ]]; then
  AGENT_ARGS+=(--session "$SESSION")
fi

# Point agent's run_python at topml so helpers have numpy/pyarrow/triplet_ml
TOPML_PYTHON=$(conda run -n topml python -c "import sys; print(sys.executable)" 2>/dev/null)
export PYTHON="$TOPML_PYTHON"

echo "=== topreco-agent ==="
echo "  workspace : $SELF_DIR"
echo "  config    : $CONFIG"
if [[ -f "$PROMPT_OR_FILE" ]]; then
  echo "  prompt    : $PROMPT_OR_FILE"
else
  echo "  prompt    : (inline)"
fi
[[ -n "$SESSION" ]] && echo "  session   : $SESSION"
echo ""

cd "$SELF_DIR"
PYTHONPATH="$AGENT_DIR" conda run -n topml python -m agent_kit "${AGENT_ARGS[@]}"
