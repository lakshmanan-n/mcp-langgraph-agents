# VectorDBaaS — Chief Architect Briefing
### Why Control Plane + Data Plane, and What Every Box Does

---

## 1. Why Do We Need a Control Plane and Data Plane?

### The 30-second answer for the chief architect:

> "We need **central governance without centralised data**. The control plane gives us one place to enforce embedding standards, contracts, lineage, and cost tracking across the bank. The data planes give each platform (CIB, WPB, etc.) local vector storage that honours residency, performance, and engine choice — without recreating today's fragmented, ungoverned mess."

### The three alternatives we rejected (and why):

| Pattern | Why it fails |
|---------|-------------|
| **Single monolithic vector store** | Can't honour residency or platform-local performance; single blast radius; couples all AI use cases to one engine choice; single team bottleneck |
| **Per-use-case vector stores** (today's state) | Already proven painful — no governance, no cost transparency, no embedding consistency, no lineage, duplicated infrastructure |
| **Federated-only (per-platform, no centre)** | Matches platform reality but recreates fragmentation — no embedding governance, no service registry, no consistent retrieval-time controls, no chargeback |

### What hub-and-spoke solves:

```
WITHOUT hub-and-spoke (today):         WITH hub-and-spoke (proposed):

CIB builds its own vector store        CIB operates a data plane
WPB builds its own vector store    →   WPB operates a data plane
R&C builds its own vector store        R&C operates a data plane
                                        ↑   ↑   ↑
No shared standards                    ONE control plane
No shared embedding models              governs ALL of them
No lineage                    
No cost visibility            
No quality monitoring         
```

---

## 2. Control Plane — Box by Box

The control plane is the **brain** of the service. It never stores vectors. It governs everything.

> **Owned by:** AI for Tech  
> **Operates:** Centrally (one instance for the bank)

### Box 1: Service Registry & Contracts

| Aspect | Detail |
|--------|--------|
| **What it is** | The canonical record of every vector collection in the bank |
| **What it holds** | Collection name, owner, tenant, use case, schema, classification ceiling, SLA targets, retention policy, residency, embedding model, cost class |
| **Why it matters** | Without this, nobody knows what vector collections exist, who owns them, what data they hold, or what SLAs apply. Today, vector stores are invisible — no registry, no contracts |
| **Chief architect angle** | This is the equivalent of a service catalogue for vector capability. Every collection has a contract before it goes live. No contract = no collection |
| **Example** | CIB's "Codify the Bank" team registers a collection: `cib-codify-docs`, owner: CTB team, classification: Confidential, residency: UK, embedding model: text-embedding-005, SLA: p95 < 200ms |

### Box 2: Embedding Model Registry & Governance

| Aspect | Detail |
|--------|--------|
| **What it is** | The catalogue of approved embedding models with versions, deprecation policies, and drift signals |
| **Why it matters** | **This is the single most important control in the service.** Embedding model choice is the dominant lever for retrieval quality. If teams use different models, their vectors are non-comparable, search quality diverges, and you can't manage drift or refresh |
| **What it prevents** | Unapproved models entering production; version sprawl; silent quality degradation after model updates |
| **How it works** | Group AI approves models via MCP → models registered here with version, policy, and drift thresholds → all data planes must use registered models → when a model is deprecated, the control plane orchestrates re-embedding |
| **Chief architect angle** | Think of it as the "approved parts list" for AI. You wouldn't let each team choose their own encryption algorithm — same principle for embeddings |

### Box 3: Index Lifecycle Service

| Aspect | Detail |
|--------|--------|
| **What it is** | Orchestrates the lifecycle of vector indexes across all data planes |
| **What it does** | Provisioning new collections, triggering re-index when embedding models are refreshed, scheduled rebuilds, retention-driven purge, restore from upstream source-of-truth |
| **Why it matters** | Vectors are derived assets — they can and must be rebuilt when embedding models change. Without centralised lifecycle management, each team manages this manually (or doesn't) |
| **Chief architect angle** | This is the deployment and lifecycle orchestrator. When we upgrade from embedding model v4 to v5, this service coordinates the re-embed across every affected collection, verifies quality hasn't regressed, and promotes to production |

### Box 4: Classification & DLP Gate

| Aspect | Detail |
|--------|--------|
| **What it is** | A gate that blocks ingestion of any content that doesn't carry classification and provenance metadata |
| **Why it matters** | In a regulated bank, you cannot embed content you can't classify. If un-classified or mis-classified content enters a vector collection, you have a governance breach that's invisible at retrieval time |
| **How it works** | Every record submitted for ingestion must carry: source classification, provenance (where it came from), source ID, and timestamp. If any are missing → rejected |
| **Chief architect angle** | This is the "no classification, no entry" gate. It enforces upstream obligations from Layers 2-3 of the reference architecture |

### Box 5: Lineage & Metadata Publisher

| Aspect | Detail |
|--------|--------|
| **What it is** | Publishes lineage events and metadata to the enterprise catalogue and, where applicable, publishes semantic products to Fabric |
| **Why it matters** | Vector collections are invisible to the wider data community today. This makes them discoverable, traceable, and auditable |
| **What it publishes** | Collection creation/update/retirement events, refresh events, reindex events, embedding model changes, Fabric product publication |
| **Chief architect angle** | This connects VectorDBaaS to the enterprise data governance ecosystem. Every vector collection appears in the catalogue with full lineage — just like structured data |

### Box 6: Retrieval Quality Governance

| Aspect | Detail |
|--------|--------|
| **What it is** | Framework for monitoring and enforcing retrieval quality baselines |
| **Why it matters** | **A service can be fully governance-compliant — meeting all classification, lineage, entitlement, and audit requirements — and still fail if retrieval results are poor.** This closes that gap |
| **How it works** | Each collection defines a quality baseline (e.g. Recall@10 ≥ 0.85) against a benchmark set. Sampled relevance evaluation runs on schedule. Degradation triggers alerts. Quality regression blocks embedding model promotion |
| **Chief architect angle** | This is the difference between "architecturally compliant" and "actually useful". Without this, we could build a perfectly governed service that nobody trusts because search results are poor |

### Box 7: AI Observability & FinOps

| Aspect | Detail |
|--------|--------|
| **What it is** | Unified observability and cost management for the entire service |
| **What it tracks** | Usage (calls, records, embeddings), latency (p50/p95/p99), retrieval quality metrics, cost (embedding inference, storage, compute, egress), governance signals (blocked requests, failed entitlements) |
| **Why it matters** | If consumption is not measurable, governance is theoretical. Without this, costs grow without attribution and service viability cannot be demonstrated |
| **Chargeback model** | Tenants charged on transparent unit basis: per million embeddings, per million queries, per GB stored, per index hour |
| **Chief architect angle** | This makes the service fundable and sustainable. Every collection's cost is attributable. Every query is measured. FinOps is not an afterthought — it's a first-class capability |

---

## 3. Data Plane — Box by Box

The data plane is the **muscle** of the service. It stores vectors, serves queries, and enforces runtime controls.

> **Owned by:** Each data platform team (CIB, WPB, R&C, etc.)  
> **Operates:** Locally within each platform (one data plane per platform/region)  
> **Engine choice:** Implementation detail — can be pgvector, Vertex AI Search, or future approved engines

### Box 1: Vector Engine

| Aspect | Detail |
|--------|--------|
| **What it is** | The actual vector database engine — pgvector, Vertex AI Search, or a future approved engine |
| **What it does** | Stores vector collections, maintains ANN indexes, executes similarity search |
| **Why engine choice is abstracted** | Different platforms may need different engines. CIB might use pgvector (fits their Postgres ecosystem). WPB might use Vertex AI Search (fits GCP). The service contract is the same regardless of engine |
| **Chief architect angle** | We're not picking one engine for the bank. We're abstracting engine choice behind the data-plane contract so platforms can make platform-appropriate choices without breaking governance |

### Box 2: Embedding Execution Service

| Aspect | Detail |
|--------|--------|
| **What it is** | Performs embedding (converting text/content into vectors) by calling Group AI's models via MCP |
| **What it does NOT do** | Host models locally. All embedding inference goes through Group AI via MCP — no local model hosting, no shadow models |
| **Why via MCP** | Single point of model governance. Consistent with L5 (Governed AI Integration) of the reference architecture. Prevents unapproved models entering production |
| **Chief architect angle** | This is why AD-03 exists: "All embedding inference goes through Group AI via MCP — no local model hosting." If we allowed local models, the embedding registry becomes meaningless |

### Box 3: Retrieval API

| Aspect | Detail |
|--------|--------|
| **What it is** | The API that consumers call to search vector collections |
| **What it supports** | Filtered vector search (with metadata filters), hybrid search hooks (vector + structured filters), ranked results with provenance returned for every hit |
| **Key design point** | Every result includes provenance (where the source content came from). This is mandatory for downstream RAG citation and for audit |
| **Chief architect angle** | Consumers call this API — they never talk to the vector engine directly. The API enforces entitlement, classification, and provenance at every call |

### Box 4: Runtime Access & Policy Enforcement

| Aspect | Detail |
|--------|--------|
| **What it is** | The runtime enforcement layer that checks every retrieval call against the caller's entitlements and the collection's policies |
| **What it checks** | Caller identity (via Enterprise IAM), group memberships, collection classification ceiling, provenance requirements, residency compliance |
| **Why it matters** | In a regulated bank, you can't serve vector search results to someone who isn't entitled to see the underlying content. This enforces that at every call, not just at onboarding |
| **Chief architect angle** | This is the equivalent of row-level security in BigQuery, but for vector retrieval. Every query is authenticated, authorised, and audited |

### Box 5: Cache & Session Store

| Aspect | Detail |
|--------|--------|
| **What it is** | Latency-sensitive working memory for re-ranked results, agent state, and short-lived embeddings |
| **Why it exists** | RAG and agentic workflows need sub-second retrieval. Caching frequent queries and maintaining session state avoids repeated embedding inference and re-ranking |
| **Chief architect angle** | This is an operational optimisation, not a governance concern. It reduces latency and cost for high-frequency retrieval patterns |

---

## 4. How Control Plane and Data Plane Work Together

```
TENANT REQUEST                          RUNTIME QUERY
"I need vector search for              "What are the CIB margin
 regulatory documents"                  requirements?"
         │                                      │
         ▼                                      ▼
   ┌─────────────┐                      ┌──────────────┐
   │ CONTROL PLANE│                      │  DATA PLANE  │
   │              │                      │              │
   │ 1. Review    │  ──── contract ───▶  │ 1. Authenticate
   │ 2. Register  │                      │ 2. Check entitlement
   │ 3. Provision │                      │ 3. Embed query (via MCP)
   │ 4. Monitor   │  ◀── metrics ─────  │ 4. Vector search
   │ 5. Chargeback│                      │ 5. Return + provenance
   └─────────────┘                      │ 6. Audit log
                                        └──────────────┘

   GOVERNS                               EXECUTES
   (what, who, how, quality)             (store, search, enforce)
```

### The split in one sentence:

> **Control plane decides the rules. Data plane enforces them at runtime.**

---

## 5. Likely Chief Architect Questions — Prepared Answers

### Q: "Why not just use one managed vector DB for the whole bank?"

> "Residency and performance. CIB UK data can't sit in a US-hosted service. WPB's GCP workloads need a GCP-native engine. A single monolithic store creates a single blast radius and couples every AI use case to one engine. Hub-and-spoke gives us central governance without centralised data."

### Q: "Who owns this? Is AI for Tech taking over data platforms?"

> "No. AI for Tech owns the control plane — standards, contracts, embedding governance, onboarding. Data platform teams continue to own and operate their local data planes. Group AI owns the embedding models. Security, governance, and risk own their policies. The service enforces those policies but doesn't define them."

### Q: "What about pgvector vs Vertex AI Search?"

> "Both are approved. Engine choice is an implementation detail behind the data-plane contract. CIB can use pgvector, WPB can use Vertex AI Search. The control plane doesn't care which engine — it governs the contract, not the product. When new open-source engines are approved, they slot in the same way."

### Q: "What if retrieval quality is poor?"

> "Section 9.1 — Retrieval Quality Governance. Every collection has a quality baseline, benchmark set, and relevance monitoring. Quality regression blocks embedding model promotion. This is a first-class capability, not an afterthought. A governance-compliant service that returns poor results is a failed service."

### Q: "How do you charge for this?"

> "Transparent unit economics: per million embeddings, per million queries, per GB stored, per index hour. Every collection's cost is attributable. Chargeback is rehearsed in Phase 2 and goes live in Phase 5. Unattributable costs (control plane, registry) are recovered as proportional service overhead."

### Q: "What's the risk if we don't do this?"

> "We already have the risk — multiple teams building their own vector stores with different engines, different embedding models, no lineage, no cost visibility, no quality monitoring. Every new use case adds to the fragmentation. The question isn't whether we can afford to build this service — it's whether we can afford not to."

### Q: "Is this a settled standard?"

> "No — it's a proposed enterprise pattern for endorsement. We're asking the working group and architecture forum to endorse the shape, the ownership model, and the roadmap direction. It becomes a standard through adoption and governance, not by declaration."

---

## 6. Key Numbers to Have Ready

| Metric | Value |
|--------|-------|
| Approved vector engines | 2 (pgvector, Vertex AI Search) + open-source pipeline |
| Architectural decisions documented | 12 (AD-01 to AD-12) |
| Open questions for working group | 9 (OQ-01 to OQ-09) |
| Risks with mitigations | 9 |
| Roadmap phases | 6 (P0–P5) |
| Control plane capabilities | 7 boxes |
| Data plane capabilities | 5 boxes per plane |
| Ownership parties | 6 (AI for Tech, Data Platforms, Group AI, Data Gov, Security, Risk) |
