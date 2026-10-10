# Project Codex resources

This directory contains repository-specific Codex resources that should be
version-controlled when they are safe to share.

- Keep the project overview and doc navigator in the root `AGENTS.md`.
- Keep reusable skills in the shared project tree `.agents/skills/`. Codex
  reads that directory; do not install Agent Ledger skills only under
  `.codex/skills/` or `~/.codex/skills/`.
- `config.toml` holds project-scoped Codex MCP servers. Launch local servers
  through a wrapper that reads the ignored `.env`. Do not place tokens, API
  keys, OAuth grants, or personal machine settings here.

Authenticated OAuth sessions still live in the local Codex client. After
cloning, reconnect remote MCPs such as Render and Postman inside Codex.
