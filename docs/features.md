# Agent Orchestration MVP — Single To‑Do (Steps 1–11)

**Objective:** Ship one UI that orchestrates Agent Builder + Avatar Chatbot + custom RAG + BudgetBot, with swappable personas (Teller, Exec, Kiosk, Budget). Keep it lean, shippable, and monetization‑ready.

> Legend: \[ ] TODO  \[\~] In Progress  \[x] Done

---

## 1) Define Persona Packs

**Goal:** Describe behavior, tone, data scope, tools, and UI modules per persona.

* **Tasks**

  * [ ] Create `personaPacks/`: `teller-v1.json`, `exec-v1.json`, `kiosk-v1.json`, `budget-v1.json`.
  * [ ] Fields: `displayName`, `goals[]`, `guardrails{}`, `ragNamespaces[]`, `tools[]`, `ui.modules[]`, `voice{}`.
  * [ ] Add schema validation (zod/pydantic) + loader.
* **Deliverables**: Persona JSONs, schema, loader function.
* **DoD**: Switching personas hot‑loads allowed tools & namespaces without server restart.

---

## 2) Tool Contracts & Mock Stubs

**Goal:** Stable interfaces so agents don’t depend on vendor SDKs.

* **Tasks**

  * [ ] Define TypeScript contracts:

    * `rag.search(query, k, namespaces, userId)`
    * `budget.analyze(userId, horizonDays)`
    * `crm.lookup(identifier)`
    * `kyc.verify(userId, docRefs)`
    * `payments.offerPreview(userId, productId)`
    * `avatar.speak(text, personaVoice, ssml)`
  * [ ] Implement mock adapters/stubs; gate with feature flags.
* **Deliverables**: `/lib/tools.d.ts`, `/server/tools/*` stubs.
* **DoD**: Orchestrator calls each stub end‑to‑end locally.

---

## 3) Vector Store & RAG Loader

**Goal:** Namespaced doc retrieval for global/bank/role/user content.

* **Tasks**

  * [ ] Choose store (Qdrant/Weaviate/pgvector). Start with Qdrant (Docker compose).
  * [ ] Build loader: PDF/MD → chunk → embed → upsert (`namespace` tags).
  * [ ] Admin API: `POST /rag/upsert` with namespace.
  * [ ] Implement `rag.search` → `{id, text, source, score}`.
* **Deliverables**: Embedding script, upsert API, search fn.
* **DoD**: Queries return 3–5 relevant chunks with scores per namespace.

---

## 4) Orchestrator API (`/orchestrate`)

**Goal:** Single entrypoint that routes persona‑scoped tool calls.

* **Tasks**

  * [ ] `POST /orchestrate { persona, user_id, messages[], tools_hint[] }`.
  * [ ] Policy guard enforces allowed tools & data scopes from persona pack.
  * [ ] Function‑calling loop: LLM plans → router executes → assemble reply.
  * [ ] Streaming via SSE/WebSocket for tokens + tool events.
* **Deliverables**: FastAPI route, router, policy module.
* **DoD**: Echo flow works with `rag.search` + ≥1 tool per persona.

---

## 5) Prompting & Memory Context Builder

**Goal:** Consistent persona behavior with controllable context.

* **Tasks**

  * [ ] System prompt composer: persona → goals → guardrails → tool manifest.
  * [ ] Context builder: short‑term chat (with truncation), top‑K RAG chunks, user prefs.
  * [ ] Output parser for function calls + final message.
* **Deliverables**: Prompt templates, composer, context builder.
* **DoD**: Swapping personas changes tone & tools with no code edits.

---

## 6) Next.js UI (Chat + Persona Switcher + Tools Rail)

**Goal:** One UI, many faces.

* **Tasks**

  * [ ] Chat pane with function‑call event timeline.
  * [ ] Persona switcher (Teller / Exec / Kiosk / Budget).
  * [ ] Right‑rail modules: Docs (RAG hits), Accounts/CRM, **Offers** panel.
  * [ ] Feature flag `avatarEnabled` → media player for audio/video replies.
* **Deliverables**: Pages, components, shadcn cards, hooks.
* **DoD**: Chat works, persona switching mid‑session preserves context.

---

## 7) Offer Engine v0 + Catalog

**Goal:** Turn every conversation into a store.

* **Tasks**

  * [ ] `offers/catalog.json`: `product_id`, rules (segments/minBalance), copy, CTA.
  * [ ] Rules evaluator: `evaluate(user, session, insights) → top 1–2 offers`.
  * [ ] Track CTR & conversions.
* **Deliverables**: Catalog JSON, evaluator, UI panel.
* **DoD**: Personalized offers render; clicks log with metadata.

---

## 8) Avatar/TTS Integration

**Goal:** Optional voice/video replies per persona.

* **Tasks**

  * [ ] Implement `avatar.speak` adapter (ElevenLabs/SadTalker or stub).
  * [ ] UI toggle; display audio/video URL + transcript.
  * [ ] Cache media by hash(text+voice).
* **Deliverables**: Adapter, media proxy route, player component.
* **DoD**: Persona reply can play voice/video when enabled.

---

## 9) Session Memory (Redis) + Long‑Term Refs

**Goal:** Useful continuity without runaway context.

* **Tasks**

  * [ ] Redis for short‑term turns + tool results (TTL).
  * [ ] Persist long‑term refs: vector IDs + user traits/segments in Mongo.
  * [ ] Memory hygiene: truncation + PII masking on stored text.
* **Deliverables**: Memory service, Redis client, models.
* **DoD**: Sessions resume with recall of key facts + RAG refs.

---

## 10) Events & Analytics

**Goal:** Know what prints money.

* **Tasks**

  * [ ] Event schema: persona, tools, latency, tokens, RAG sources.
  * [ ] Dashboard (Grafana/Metabase) for CTR, handle time, containment %, conversion.
  * [ ] AB flags for prompt variants.
* **Deliverables**: Logger, exporter, simple dashboard.
* **DoD**: Weekly CSV export of pilot metrics is possible.

---

## 11) Security, Consents & Governance

**Goal:** Safe‑by‑default and demo‑ready.

* **Tasks**

  * [ ] Consent gates before CRM/Budget access.
  * [ ] I/O filters: mask PAN/SIN; redact sensitive text pre‑LLM.
  * [ ] Audit trail per tool call (hashes + source IDs) with export.
  * [ ] Feature flags + kill‑switch per persona/tool.
* **Deliverables**: Consent UI, middleware, audit writer, flags.
* **DoD**: Security checklist passes; audit can reconstruct any reply.

---

### Notes

* Keep adapters thin; vendors swap behind tool contracts.
* Log everything; analytics funds the roadmap.
* Proposed build order: 1 → 6 → 4 → 5 → 3 → 7 → 9 → 8 → 10 → 11.
