#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# The agent copies this file and edits the steps below. The user runs it in
# their own interactive terminal (the agent's shell has no terminal for
# `read`) and pastes the final "--- Captured ---" block back to the agent.
#
# Usage:
#   bash hitl-loop.sh
#
# Two helpers:
#   step "<instruction>"          → show instruction, wait for Enter
#   capture VAR "<question>"      → show question, read one line into VAR
#
# Answers are one line each; ask for multi-line output to be pasted as one
# line or saved to a file whose path is captured instead.
#
# At the end, captured values are printed as KEY=VALUE for the agent to parse.
# Capture observations only; leave signing in and secrets to a `step`.

set -euo pipefail

if [[ ! -t 0 ]]; then
  echo "Run this script in an interactive terminal; it reads answers from stdin." >&2
  exit 1
fi

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------

step "Open the app at http://localhost:3000 and sign in."

capture ERRORED "Click the 'Export' button. Did it throw an error? (y/n)"

capture ERROR_MSG "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
