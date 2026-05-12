# Presentation Notes — Full Deck

**Audience:** Group Head for Data Platforms · Group AI Platforms  
**Deck flow:** Ref arch intro → OKR → Deep dive → Core capabilities → VectorDBaaS → Codify the Bank  
**Target duration:** 25–30 minutes including discussion  

---

## Before You Start — Audience Framing

These two stakeholders care about different things. Your notes must address both:

| Stakeholder | What they care about | What they're listening for |
|---|---|---|
| **Group Head, Data Platforms** | Where does this land on my platforms? Who operates it? What does federation look like? | "This runs on your infrastructure, under your operating model, with contracts we define centrally." |
| **Group AI Platforms** | Are you building a shadow AI stack? Do you own models? How do you consume my services? | "We consume your models. You own the embedding lifecycle. We provide the vector service layer." |

> [!IMPORTANT]
> **The single most important message for this audience:**  
> This workstream does not build a competing platform. It defines the enterprise capability model for unstructured data and delivers priority shared services — VectorDBaaS being the first — that deploy *within* existing data platforms and *consume* Group AI services.

---

## Slide 1 — Reference Architecture Introduction

**Purpose:** Set the context. Explain why a reference architecture exists and what it covers.

### What to say (~3 min)

> "Before we get into specifics, let me set the architectural context.
>
> The bank has a strong structured data platform — Fabric, catalogues, governed data products. For unstructured data, we don't have that yet. Every use case builds its own pipeline, its own ingestion, its own vector store, its own retrieval logic. That's where this workstream comes in.
>
> We've defined a reference architecture — not a product design, not a platform blueprint — a capability model. It describes the lifecycle that unstructured data needs to go through to become useful and governed: from source onboarding, through preparation and semantic processing, to governed retrieval and Fabric publication.
>
> Think of it as the equivalent of what already exists for structured data — but for documents, audio, transcripts, operational records, and the AI-derived products that come out of processing them."

### Key phrases to use
- "Enterprise capability model" — not "platform"
- "Lifecycle" — source → ingest → prepare → process → store → publish → consume
- "Governed" — this is not a raw data pipeline; governance is embedded

### What to avoid
- Don't say "we are building a platform"
- Don't list all 8 architecture layers in detail — that's the deep dive slide
- Don't get into technology choices here

### Transition to next slide
> "So that's the architectural framing. Let me show you the outcomes we're targeting."

---

## Slide 2 — OKR

**Purpose:** Connect the architecture to measurable business outcomes.

### What to say (~2 min)

> "These are the objectives we're working toward — not project milestones, but enterprise outcomes.
>
> [Walk through the OKRs on the slide]
>
> The common thread across all of these is: we are moving from individual use cases solving their own problems to shared, governed, reusable capability. That's the business value — reduced duplication, stronger controls, and faster onboarding for every subsequent use case."

### Hooks for this audience

**For Data Platforms:**
> "One of the key results here is federated adoption — your platforms host the data planes. This isn't a central build that bypasses your infrastructure."

**For Group AI:**
> "You'll notice we don't have OKRs around model selection or embedding lifecycle — because that's yours. Our outcomes depend on consuming your services, not duplicating them."

### Transition
> "Let me now walk you through what the architecture actually looks like."

---

## Slide 3 — Deep Dive: Reference Architecture

**Purpose:** Show the full lifecycle visually. Establish the architecture vocabulary.

### What to say (~4 min)

> "This is the full reference architecture. Eight lifecycle layers plus a cross-cutting control plane.
>
> I'm not going to walk through every box. What matters is the flow — left to right:
>
> **Sources** come in from heterogeneous domains — documents, audio, communications, operational systems. We don't own the sources.
>
> **Ingestion and onboarding** is the first control boundary. This is where policy-aware routing decides how content is handled — by sensitivity, residency, trust level. This is the gate.
>
> **Preparation** produces canonical, governed content. Redaction and classification happen here — before anything enters semantic processing. That's a non-negotiable.
>
> **Orchestration and semantic processing** is where content becomes useful — chunking, embedding, graph build, entity extraction. This is where we consume Group AI's embedding models via MCP. We orchestrate; Group AI provides the models.
>
> **Persistence** is polyglot — raw, metadata, vector, graph, cache. VectorDBaaS lives here as a governed shared service.
>
> **Fabric publication** is where unstructured-derived products become discoverable and governed to the same standard as structured data. This is the gap we're closing — today, unstructured products don't go through Fabric.
>
> **Retrieval and consumption** is the end — governed retrieval for RAG, agentic use cases, and analytics. Entitlement and provenance are enforced at retrieval time, not just at publishing time.
>
> And underneath all of this — identity, DLP, lineage, audit, encryption, residency, responsible AI. Not optional extras. Enterprise controls."

### Key hooks

**For Data Platforms:**
> "Layers 5–7 — persistence, Fabric, retrieval — are where your platforms play. We define the service contract and control plane; your platforms provide the execution environment."

**For Group AI:**
> "Layer 4 is where we integrate. We consume your models through MCP. We don't host models, we don't manage model lifecycle, we don't select embedding models. That's your domain."

### What to avoid
- Don't read every box — point and summarise
- Don't get into technology choices (pgvector, Vertex AI, etc.) — those are implementation details
- Don't let this slide become a 10-minute walkthrough — 4 minutes maximum

### Transition
> "So that's the target model. The question is: what does it change for the bank today? Let me show you."

---

## Slide 4 — Core Capabilities: What This Workstream Changes

**Purpose:** This is the strategic punchline. Three structural shifts, each closing a named risk.

### What to say (~4 min)

> "This slide answers the 'so what' question. What actually changes for the bank?
>
> Three shifts. Left to right.
>
> **First: fragmented intake and preparation becomes a governed standard.**
>
> Today, every use case builds its own ingestion. Redaction is applied inconsistently, or not at all, before content enters AI pipelines. That's a first-order control weakness. The workstream shapes a shared onboarding and preparation pattern with an enforced redaction gate.
>
> The risk this closes: sensitive-data leakage into embeddings and graphs. That's not a theoretical risk — it's a structural architecture gap.
>
> **Second: use-case-specific semantic services become shared enterprise capability.**
>
> Today, each use case makes its own chunking, embedding, and vector decisions. Different models, different indexes, no portability, no cost attribution. The workstream shapes shared semantic services — including VectorDBaaS — with approved model consumption through Group AI.
>
> The risk this closes: duplicated investment. Non-reusable semantic capability. Rising total cost of ownership.
>
> **Third: ungoverned retrieval and publication becomes enterprise-standard.**
>
> Today, structured data has Fabric. Unstructured data does not. That means unstructured-derived products — the things AI actually uses — sit outside the enterprise data product standard. The workstream shapes Fabric publication for unstructured-derived products and retrieval-time governance.
>
> The risk this closes: control divergence. The unstructured estate remains a permanent exception to the enterprise model."

### The line to land
> "And the positioning statement at the bottom — this is not a monolithic platform build. It is progressive capability shaping. VectorDBaaS is one priority shared service within the wider target model."

### Audience-specific hooks

**For Data Platforms:**
> "Shift 2 is where your platforms benefit most. Shared semantic services and VectorDBaaS reduce the fragmented vector infrastructure your teams are currently standing up independently per use case."

**For Group AI:**
> "Shift 2 explicitly uses your models. 'Approved model consumption through Group AI' — that's on the slide. We don't select models, we consume what you approve."

### Transition
> "Let me now zoom into VectorDBaaS — the priority shared service from that second shift."

---

## Slide 5 — VectorDBaaS

**Purpose:** Explain VectorDBaaS as a governed service pattern. Show where data planes sit.

### What to say (~4 min)

> "VectorDBaaS is a governed shared service for enterprise vector persistence and retrieval. I want to be precise about what it is and what it is not.
>
> Five design decisions on the left:
>
> **Hub-and-spoke.** Central control plane sets standards. Data planes execute within each platform.
>
> **Data stays local.** Vectors remain within each platform boundary. We don't extract vectors to a central location. Residency is maintained.
>
> **Group AI model path.** Embeddings are consumed from Group AI via MCP. We don't host, select, or manage embedding models. That's Group AI's domain.
>
> **Dual access model.** Direct retrieval for latency-sensitive AI use cases. Fabric publication for governed data products.
>
> **Evidence-led rollout.** Mobilise, prove on one platform, harden the service model, then extend. No fixed dates until the pattern is validated.
>
> And the blue box — this is the key architectural statement:
>
> *'VectorDBaaS provides the governed vector service layer; approved embedding model ownership remains with Group AI.'*
>
> On the right — the visual. Control plane at the top, centrally owned. Three governance clusters: service governance, model and lifecycle governance, control and operations. Below that, federated data planes — one per data platform. CIB, WPB, Platform N. Each data plane contains the same five components. Vectors never leave the plane.
>
> And at the bottom — the enterprise services we consume. Group AI for embeddings. Enterprise catalogue. Fabric. IAM. DLP. These are dependencies, not things we own."

### Critical hooks

**For Data Platforms — this is your slide:**
> "Each data plane runs within your platform. You provide the execution environment. We provide the service contract, lifecycle governance, and control-plane standards. Engine choice — pgvector, Vertex AI Search, whatever — is an implementation detail behind the data-plane contract. That's your decision within your platform."

**For Group AI — this is your boundary:**
> "We explicitly do not own embedding models. We consume what you approve. The control plane includes an embedding model registry — that's a governance instrument, not a model store. Model selection, versioning, refresh, deprecation — those remain with you."

### Transition
> "Let me now show you what this looks like in practice — with a real use case."

---

## Slide 6 — Codify the Bank Reference Use Case

**Purpose:** Ground the architecture in reality. Show it's not just theory.

### What to say (~3 min)

> "Codifying the Bank is the reference use case we're using to validate the architecture end to end.
>
> It's a document-centric knowledge workflow. Documents are ingested, prepared, reauthored with AI assistance, validated, reviewed with human-in-the-loop, then processed into knowledge graph and embeddings, and served through hybrid retrieval — graph plus vector.
>
> Why does this matter? Three reasons:
>
> **First,** it validates the full lifecycle — source to retrieval. Every layer of the reference architecture is exercised.
>
> **Second,** it demonstrates graph and vector coexistence. Not everything is a vector search problem. Some content needs entity relationships and structured knowledge. This use case proves both can work together under a common architecture.
>
> **Third,** it proves that HITL, provenance, lineage, and auditability are not optional add-ons. In a regulated bank, AI-generated content must be reviewed before it's published as authoritative. This use case builds that into the workflow, not around it.
>
> What it proves for the workstream: a repeatable onboarding pattern for document-centric use cases, a practical example of where VectorDBaaS becomes the standard vector capability, and evidence that deterministic workflow, AI services, knowledge graph, and retrieval can be composed under enterprise controls."

### Key hooks

**For Data Platforms:**
> "This is where the first data plane gets validated. The vector and graph persistence in this use case is where we prove the data-plane contract works in practice."

**For Group AI:**
> "This use case consumes your embedding models and your AI platform services through MCP. It's the first practical validation of that integration path."

### What to avoid
- Don't get into implementation details (LangGraph, specific models, etc.)
- Don't treat this as a project status update — it's architecture evidence
- Don't oversell — say "reference use case" not "production system"

---

## Overall Business Value — The Thread That Runs Through Every Slide

If the audience asks "what's the business value?" at any point, this is the answer:

> "Today, every AI use case that touches unstructured data builds its own pipeline, its own vector infrastructure, its own retrieval logic. That produces three problems:
>
> 1. **Cost** — duplicated investment across use cases with no reuse
> 2. **Control** — inconsistent governance, no assured redaction, no retrieval-time entitlement
> 3. **Speed** — every new use case starts from zero instead of consuming shared services
>
> This workstream changes that. It defines the enterprise capability model, shapes the shared services, and delivers VectorDBaaS as the first priority service. The business value is: every subsequent use case onboards faster, costs less, and is governed from day one."

---

## Timing Guide

| Slide | Topic | Time | Cumulative |
|---|---|---|---|
| 1 | Ref arch intro | 3 min | 3 min |
| 2 | OKR | 2 min | 5 min |
| 3 | Deep dive | 4 min | 9 min |
| 4 | Core capabilities | 4 min | 13 min |
| 5 | VectorDBaaS | 4 min | 17 min |
| 6 | Codify the Bank | 3 min | 20 min |
| — | Discussion | 10 min | 30 min |

> [!TIP]
> **If you're running short on time,** the two slides you cannot skip are **Slide 4** (core capabilities — the strategic punchline) and **Slide 5** (VectorDBaaS — the service they need to sponsor). Slides 1–3 can be summarised verbally in 2 minutes. Slide 6 can become a follow-up.
