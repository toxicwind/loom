# Visor lane (tauvisor/kappavisor) — Loom fork notes

**Status:** product mapping, 2026-11-02 (arc: loom-visor-advisor)

`toxicwind/loom` is an estate fork of `rjwalters/loom` — the label-driven
AI orchestration tool (Curator → Builder → Judge → Doctor → Merge, worktrees,
`loom-daemon` DispatchSweep, 30 MCP tools). **This fork IS the first-class
Loom product**; the scaffolding attempt of a competing `barn/products/loom`
README was reverted in favor of this upstream (adopted verbatim).

## Where the visor lane lives

- **tauvisor** — tau's live advisor role (`~/.tau/agent/TAUVISOR.yml`),
  sandbox `read-only` by default, main-aware via the async git-state hook,
  enforcement in the runtime (anomaly #73 lesson). Config lives in tau, not
  Loom.
- **kappavisor** — kappa mirror (no advisor today; when it lands it MUST
  mirror: read-only default, main-aware, runtime-enforced).

## Why Loom is the right home for visor work

Loom's role system (`/loom:curator`, `/loom:judge`, `/loom:doctor`,
`/loom:auditor`) IS a visor pattern — a trusted reviewer layer over agent
writes. tauvisor/kappavisor are the estate-native equivalents on the
olympus side; Loom's roles are the forge-native ones. Do not duplicate:
- Use Loom roles for forge-coordinated sweeps.
- Use tauvisor/kappavisor for transcript-level advisor review.
- The shared doctrine: read-only by default, main-aware, runtime-enforced.

## Fork ownership

Upstream: `rjwalters/loom` (MIT © 2025 Robb Walters). Estate fork:
`toxicwind/loom`. Future visor-lane work (kappavisor scaffold, tauvisor
wiring) lands here + in `pens/olympus/products/tau`, never a third checkout.