#!/usr/bin/env bash
# Convenience wrapper to start the Loom daemon from your repository root.
#
# ── VISOR LANE (estate banner) ───────────────────────────────────────────────
#   tauvisor   — tau's live advisor role (~/.tau/agent/TAUVISOR.yml):
#                read-only sandbox by default, main-aware via the async
#                git-state hook, enforcement in the runtime (anomaly #73).
#   kappavisor — kappa mirror (no advisor today; when it lands it MUST mirror:
#                read-only default, main-aware, runtime-enforced).
#   Doctrine   — read-only by default, main-aware, runtime-enforced. Loom
#                roles (/loom:curator, /loom:judge, ...) are the forge-native
#                lane; tauvisor/kappavisor are the olympus native ones.
#   Details    — docs/visor-lane.md; never a third checkout.
# ─────────────────────────────────────────────────────────────────────────────
#
# Usage:
#   ./loom.sh               # Start in normal mode
#   ./loom.sh --merge       # Force/merge mode (auto-promote + auto-merge)
#   ./loom.sh --status      # Check if daemon is running
#   ./loom.sh --stop        # Send graceful shutdown signal
#   ./loom.sh --help        # Show all options
#
# This script is a thin wrapper around .loom/scripts/start-daemon.sh, which now
# delegates to the tmux-based `.loom/bin/loom start`. Agents are spawned via
# `tmux new-session -d` on a dedicated `-L loom` socket, so they are reparented
# to the tmux server (not the invoking shell) and survive its exit. That makes
# this safe to run from inside a Claude Code session — worker sessions are never
# descendants of the session that launched them.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_DAEMON="$SCRIPT_DIR/.loom/scripts/start-daemon.sh"

if [[ ! -x "$START_DAEMON" ]]; then
    echo "Error: Loom daemon script not found at $START_DAEMON" >&2
    echo "Is Loom installed in this repository?" >&2
    exit 1
fi

exec "$START_DAEMON" "$@"
