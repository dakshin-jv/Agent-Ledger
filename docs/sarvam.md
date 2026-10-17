# Sarvam

**Read when:** Indian-language speech, text, documents, or LLM in a workflow; Sarvam service map and adoption stance.

**Do not use for:** persistence ([`render.md`](render.md)) or payments ([`paypal.md`](paypal.md)).

## Role in Agent Ledger

Sarvam provides Indian-language transcription, translation, text-to-speech, document intelligence, and language-model capabilities where a workflow needs them. Outputs are proposals or evidence unless an owner action on the case grants authority.

## Service map

Default model IDs drift; check [Sarvam API docs](https://docs.sarvam.ai/). For build-time discovery (languages, speakers, request shapes), use Sarvam MCP `sarvam_code_*` tools. Runtime actions use `sarvam_tools_*` through the policy adapter.

| Service | Official doc | Primary models | Modes | MCP tool(s) | Agent Ledger stance | Ledger use |
| --- | --- | --- | --- | --- | --- | --- |
| Speech-to-text | [STT overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview) | `saaras:v4` | sync, batch, WebSocket | `stt_transcribe` | adopted | Transcripts under consent and audit; keep audio/hash as evidence |
| Text-to-speech | [TTS overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview) | `bulbul:v3` | sync, stream | `tts_speak` | adopted | Operator- or owner-facing audio when the workflow requires it |
| Chat completion | [Chat overview](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview) | `sarvam-105b`, `sarvam-105b-conversations` | sync, stream (web API) | `llm_complete` | adopted | Intake copy and drafts; not consent or payment permission ([`procurement.md`](procurement.md)) |
| Translate | [Text processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview) | `mayura:v1` / Sarvam-Translate | sync | `translate` | adopted | Translated text; keep original input as evidence |
| Transliterate | [Text processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview) | — | sync | `transliterate` | discovery-only | Script conversion when exploring Indic intake |
| Language ID (LID) | [Text processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview) | — | sync | `identify_language` | discovery-only | Detect language before routing translate/STT/TTS |
| Document extract | [Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) | Sarvam Vision | async job | `vision_extract` | adopted | Evidence upload → structured **proposal**; original file kept ([`procurement.md`](procurement.md), `/doc-ai/v1/job/extract`) |
| Document digitize | [Document AI](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview) | Sarvam Vision | async job | `vision_digitise` | discovery-only | Full-document OCR/structure; not wired on procurement path yet |
| Document translation | [Doc translation](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview) | — | async job | `document_translate` | discovery-only | Whole-file translation with layout preserved |
| Dubbing | [Dubbing](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview) | — | async job | `dubbing_submit` | out of scope | Goods case ledger; not an adapter target |
| Voice cloning | [Voice cloning](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview) | — | — | `voice` | out of scope | Media localization; not an adapter target |
| Voice agents | [Conversations API](https://docs.sarvam.ai/api-reference/conversations) | — | deploy, outbound, analytics | — | discovery-only | Separate product (org/workspace APIs); not the default policy-adapter path |
| Text analytics | [Text processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview) | — | sync | `text_analytics` | discovery-only | NLP signals for exploration only |
| Pronunciation lexicon | [Pronunciation dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary) | `bulbul:v3` | REST | `pronunciation_create` | discovery-only | Custom TTS pronunciations; optional `dict_id` on speak |

Batch, realtime, stream, and job-status variants exist per service; names follow `sarvam_tools_<area>_*` in [Sarvam MCP](https://docs.sarvam.ai/api/developer-tools/mcp).

## Adopted capabilities

### Speech-to-text

Speech-to-text for supported languages, behind consent and audit controls. Prefer batch or WebSocket when volume or realtime intake requires it; persist transcripts only through the adapter with provenance.

### Text-to-speech

Text-to-speech for owner-facing or operator-facing audio where the workflow requires it.

### Translate

Translation between supported languages. Keep original input as evidence.

### Chat completion

Language-model completion for interpretation and intake copy. Outputs are proposals, not approval or payment permission.

Intake copy streams through the **web API** (`stream=true`; prefer `sarvam-105b-conversations`). Sourcing drafts may use `sarvam-105b`. Do not stream tokens through a Render Workflow task ([`procurement.md`](procurement.md)).

### Document extract

Field or schema-driven extraction from uploaded evidence (PDF, scan, etc.). Treat structured output as a **proposal**; the uploaded original remains authoritative evidence.

## Coding agent

- Skill: none in the shared tree
- MCP: `sarvam` (local stdio)
- Connect for service map discovery, languages, speakers, and request validation (`sarvam_code_*` / `sarvam_tools_*` per row above)

## Runtime

MCP first through the policy adapter; [Sarvam API/SDK](https://docs.sarvam.ai/) is the fallback behind the same consent, data-minimization, and audit controls.

## Secrets / env

`SARVAM_API_KEY` in [`.env.example`](../.env.example).

Official links: [Sarvam](https://www.sarvam.ai/) · [API](https://docs.sarvam.ai/) · [MCP](https://docs.sarvam.ai/api/developer-tools/mcp)

## Related

[`coding-agents.md`](coding-agents.md) · [`typesafe.md`](typesafe.md) · [`procurement.md`](procurement.md) · [`render_agent_sdk.md`](render_agent_sdk.md) (harness contract, reference only)
