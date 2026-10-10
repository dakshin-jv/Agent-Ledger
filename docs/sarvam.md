# Sarvam

**Read when:** speech-to-text, TTS, translation, or LLM completion in a workflow.

**Do not use for:** persistence ([`render.md`](render.md)) or payments ([`paypal.md`](paypal.md)).

## Role in Agent Ledger

Sarvam provides Indian-language transcription, translation, text-to-speech, and language-model capabilities where a workflow needs them.

## Features

### Transcribe

Speech-to-text for supported languages, behind consent and audit controls.

### Speak

Text-to-speech for owner-facing or operator-facing audio where the workflow requires it.

### Translate

Translation between supported languages. Keep original input as evidence.

### LLM complete

Language-model completion for interpretation tasks. Outputs are proposals, not approval or payment permission.

## Coding agent

- Skill: none in the shared tree
- MCP: `sarvam` (local stdio)
- Connect only for language/voice discovery

## Runtime

MCP first through the policy adapter; [Sarvam API/SDK](https://docs.sarvam.ai/) is the fallback behind the same consent, data-minimization, and audit controls.

## Secrets / env

`SARVAM_API_KEY` in [`.env.example`](../.env.example).

Official links: [Sarvam](https://www.sarvam.ai/) · [API](https://docs.sarvam.ai/) · [MCP](https://docs.sarvam.ai/api/developer-tools/mcp)

## Related

[`coding-agents.md`](coding-agents.md) · [`typesafe.md`](typesafe.md)
