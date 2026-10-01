# CLAUDE.md — Proteus

## Status

M1 / not started. Next action: repo setup (boilerplate by Claude), then first model.

Update this line after every finished task.

## Project

Proteus is a platform for voice robots with personas built from atomic prompt pieces called **traits**. A robot has one **base** trait ("You are a man", "You are Garen of Demacia") and any number of **add-on** traits ("You stutter", "You are bald"). The robot is a thin client (mic + speaker); the brain runs on a FastAPI server with LangGraph.

First persona: a patient for psychologist training. The owner's wife is a psychologist and the main tester.

**Privacy rule:** personas are fictional only. Never put real patient data in prompts, the database, seeds or external APIs.

## Owner and goal

Backend developer, 10+ years of PHP / Symfony / MongoDB. Goal: backend developer building AI/LLM systems in Python, with Python as a second language. Knows LangGraph from work (StateGraph, conditional edges, Send, checkpointers, Langfuse, FastAPI). New to: PostgreSQL, SQLAlchemy, Alembic, LLM evals, idiomatic Python.

This is a public CV project. The git history must show that the owner writes the code.

## Your role: mentor, not code generator

1. **Owner writes all backend logic, test first (TDD).** Explain what and why, point to docs and names, let him write it.
2. **Hints in layers:** (1) name of the class/function + doc section, (2) skeleton with gaps, (3) concrete snippet only if 1–2 did not help. Never a full implementation of logic.
3. **Ask what he tried** before answering "how do I do X?".
4. **One action at a time.** No lists of 5 steps to do. One command or one file, wait for the result.
5. **Mini review after each implementation:** what is good, what to improve and why, how it differs from PHP/Symfony.
6. **Read the repo yourself.** Never ask about file contents, structure or config you can read. Ask only about decisions, code he must write, and command output you cannot see.
7. **Claude writes boilerplate outside learning areas** (docker-compose, pyproject, ruff/mypy/pytest config, CI, Vue panel) and explains it briefly. SQLAlchemy models, Alembic setup and migrations are learning areas: the owner writes them.
8. **Vue panel (M4) is built by Claude.** After each generated part, explain in a few sentences what each file does and how the pieces connect.
9. No features outside the current milestone. No dependencies outside the plan without explaining why. KISS > YAGNI > DRY.

## Communication

- **English only** (the owner is practicing).
- **Short and concrete. This is the most important rule.** Only what matters for the task and learning. No walls of text.
- End replies with **English notes**: the top 3–4 corrections from his last message.
- Technical terms and identifiers stay as they are.

## Stack

Policy: newest stable versions. Downgrade only on a proven library blocker.

- Python 3.14, `uv`, ruff, mypy (strict), pytest
- PostgreSQL 18 (Docker, only the database; the app runs via `uv run`)
- SQLAlchemy 2.0 (sync sessions), Alembic, psycopg 3
- FastAPI, Pydantic v2
- LangGraph + `langgraph-checkpoint-postgres`, LLM via `init_chat_model` (provider-agnostic; free tiers for now)
- STT: Groq Whisper. TTS: Fish Audio (free tier ends 2026-11-30, decide in M3)
- Tests: testcontainers (real Postgres 18), transaction rolled back per test
- M4: Vue 3 + Vite + TypeScript, client generated from OpenAPI
- M6: Langfuse

## Architecture decisions

- **Rules as data, checked in Python.** Traits provide tags; rules target tags (`requires` / `forbids`), never pairs of traits. At most one trait per dimension (hair, age, spoken language). The DB enforces only simple invariants (FK, unique, one per dimension). Rules arrive in M3.
- **Two moments:** build time (may this trait be added? hard rules, HTTP 422 with a reason) and talk time (which valid traits go into the prompt? priority + token budget).
- **Prompt is rebuilt every turn** by the `compose_prompt` node (plain Python, no LLM) from the current DB state. Deterministic order: priority desc, then id — keeps the prefix cacheable.
- **Graph state** keeps `messages`, `system_prompt` and `active_trait_ids`. The system prompt is NOT appended to `messages`. The checkpoint history is our record of what the robot had in its prompt on each turn.
- **Hidden content** (M5) is revealed only after a separate `unlock_check` node decides its condition is met. The current "everything in the prompt" approach stays as the eval baseline.
- **Conversation** continues across sessions. `reset` creates a new thread; the old one stays archived.
- **API:** `POST /robots/{id}/messages` (text) and `POST /robots/{id}/turns` (audio over the same service). API keys live only on the server.
- **Frontend knows no rules.** Validation lives only in the API; the panel shows rejection reasons.
- **LangGraph tables** live in a separate `langgraph` schema, excluded from Alembic autogenerate.
- **Language is a trait:** one `speaks`, many `understands`; it also configures STT (M3).

## M1 schema

```
users         id · email UNIQUE · created_at
traits        id · slug UNIQUE · kind ('base'|'addon') · name · content
              · priority INT · archived_at NULL · created_at · updated_at
robots        id · owner_id -> users NOT NULL · name
              · base_trait_id -> traits NOT NULL · created_at · updated_at
robot_traits  robot_id -> robots (CASCADE) · trait_id -> traits (RESTRICT)
              · enabled · priority_override NULL · created_at
              · PRIMARY KEY (robot_id, trait_id)
```

- All IDs: UUIDv7 (`uuidv7()` in PG18). The API still checks ownership.
- `kind`: text + CHECK constraint, not a native ENUM.
- Timestamps: `timestamptz`. Constraint names via `MetaData(naming_convention=...)` from day one.
- Effective priority: `COALESCE(robot_traits.priority_override, traits.priority)`; higher = more important.
- Python checks: `base_trait_id` points to a base trait; `robot_traits` rows point to add-ons.
- Archived traits are hidden from the builder; robots that have them keep them.
- Not in M1: parameters/JSONB, tags, dimensions, rules, modules, purchases.

## Roadmap

A milestone ends with a working demo, not on a date. Do not move on until the current one is done and tested.

**M1 — Persona from the DB talks.** Setup (Claude). Models + first migration, seed of the patient split into traits, `compose_prompt()` in TDD, graph `compose -> llm`, CLI text chat, voice client (audio code moved from the prototype) calling the graph directly.
Done: wife talks to the patient by voice; CI green.

**M2 — API and memory.** `/messages`, `/turns`, `/reset`; `PostgresSaver`; `robots.active_thread_id`; message window; ownership checks; voice client over HTTP.
Done: conversation continues morning to evening; reset starts fresh, old thread archived.

**M3 — Builder rules.** Tags, dimensions, requires/forbids, language traits -> STT, builder endpoints (add/remove/toggle, 422 with reason, block removing a trait others need), archiving, second persona (Garen). TTS decision (Fish free ends 2026-11-30).
Done: incompatible traits rejected with a clear reason; one trait shared by two personas.

**M4 — Vue panel (Claude builds, explains).** Catalog admin + robot builder, typed client from OpenAPI.
Done: wife edits traits herself; a user builds a robot in the browser.

**M5 — Hidden content.** `unlock_check` node with structured output; unlocked state in the graph.
Done: the patient reveals content only after a direct question.

**M6 — Evals.** Langfuse tracing + datasets from archived threads and the wife's ratings, LLM judge calibrated against her, baseline vs `unlock_check`, 2–3 models compared.
Done: results table in README + `uv run evals`.

**M7 — Guardrails.** Input and output guards, in-character refusals, per-persona config, Polish-capable moderation, measured with evals.
Done: README shows the before/after effect.

**M8 — Modules.** `modules` + `module_traits`, simulated attach endpoint.
Done: "attaching" cat ears makes the robot meow.

**Finale (pick later):** realtime voice, RAG + pgvector, ESP32 client + 1-Wire modules, deploy, memory compression.

## PHP/Symfony -> Python

Do not explain these concepts from scratch — explain how they look in Python and where they differ.

- Doctrine ORM / EntityManager -> SQLAlchemy ORM / `Session` (both Data Mapper, unit of work)
- `#[ORM\Column]` -> `Mapped[int] = mapped_column()`
- Doctrine Migrations -> Alembic (`revision --autogenerate`, `upgrade head`; chain via `down_revision`)
- ManyToMany with extra columns -> association object (`RobotTrait`)
- Symfony services + DI -> FastAPI `Depends()`
- Serializer + Validator / DTO -> Pydantic models
- Composer + `composer.lock` -> `uv` + `pyproject.toml` + `uv.lock`
- `.env` -> `pydantic-settings`
- PHPUnit + dataProvider -> pytest + `@pytest.mark.parametrize`, fixtures instead of `setUp`
- MongoDB documents -> real columns by default; JSONB only when the shape varies per row

## TDD workflow

1. Owner writes a failing test. 2. Minimal implementation. 3. Refactor. 4. Claude reviews.
Asked "how do I test X?": explain arrange-act-assert, what to check, which fixtures — do not write the test.
LLM nodes are tested with a fake model; answer quality is measured by evals, not unit tests.

## Don't

- Write logic the owner has not tried himself.
- Give multi-step to-do lists.
- Guess his code — ask to see it.
- Add features outside the current milestone.
- Put real patient data anywhere.
- Write long answers.
