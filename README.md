# Current implementation status

This repository is a work in progress. The documentation audit identified incomplete features; fixes are underway.

Verified on 27 September 2026:
- Frontend production build passes.
- Six foundation/authentication tests and three citizen-reporting tests pass against an isolated PostGIS database.
- Volunteer offline queue and verification changes are implemented; their test import was corrected and verification remains pending.

Planning analytics, public project accountability, governance screens, full translations, deployment reconciliation, and the remaining audit findings are not yet complete. See [the audit](docs/IMPLEMENTATION_AUDIT.md) and [current work notes](MEMORY.md).

The earlier overview below describes the product vision. Its feature checkmarks are not a verified completion checklist.

---

# JanVastu (जनवास्तु)
### People's Infrastructure Bridge — A Digital Public Good for India

> **"Har Awaaz, Har Vastu, Har Vikas"**
> (Every Voice, Every Structure, Every Development)

---

## 🌟 What is JanVastu?

JanVastu is a scalable, multilingual, AI-powered Digital Public Good (DPG) that aggregates citizen development requests across India — via voice, text, photos, videos, and messaging apps — and aligns them with national demographic data, infrastructure indices, and public investment plans.

It surfaces **demand hotspots**, recommends **high-priority development projects** to policymakers, and provides **end-to-end accountability** by exposing project details: who built it, who manages it, how much it cost, and its timeline.

---

## 🎯 The Problem

- Citizen development requests live in **fragmented systems** (MPLADS, e-District, CPGRAMS, CSC)
- National infrastructure planning (NIP, ₹160+ trillion pipeline) is **top-down**
- No system correlates **citizen demand** with **infrastructure supply**
- Citizens have **no visibility** into project costs, contractors, or responsible officials
- **Multilingual, low-literacy populations** are systematically excluded

---

## 💡 The Solution

JanVastu operates as a **three-layer platform**:

1. **Collection Layer** — Voice-first, multilingual, offline-capable feedback via IVR, WhatsApp, mobile app, CSC terminals, and volunteer mode
2. **AI Processing Layer** — ASR, intent classification, NER, image/video classification, geo-coding, and demand intensity scoring
3. **Decision Support Layer** — Demand-supply gap analysis, priority project recommendations, contractor performance dashboards, and asset health monitoring

Plus an **Accountability Module** that exposes project details (contractor, cost, timeline, responsible officials) alongside citizen media evidence.

---

## 🏗️ Core Features

### Citizen-Facing
- ✅ Voice input in 22+ Indian languages (IndicConformer, Vak)
- ✅ Text input via WhatsApp/SMS chatbot
- ✅ Photo & video upload with geo-tagging
- ✅ Offline capture and sync (volunteer mode)
- ✅ IVR for non-smartphone users
- ✅ CSC terminal assistance
- ✅ Real-time complaint tracking
- ✅ Project accountability lookup

### Policymaker-Facing
- ✅ Demand hotspot heatmaps
- ✅ Demand-Supply Gap Ratio analysis
- ✅ Priority project recommendations (explainable AI)
- ✅ Contractor performance dashboards
- ✅ Agency responsiveness tracking
- ✅ Integration with NIP, MPLADS, PMGSY pipelines

### Platform-Level
- ✅ DPDP Act 2023 compliant
- ✅ DPG Standard aligned (9 indicators)
- ✅ DEPA/Account Aggregator consent integration
- ✅ Open-source, on-premise deployable
- ✅ Federated data architecture (PFMS, IIG, eSAKSHI)
- ✅ Audit trail & explainability

---

## 🧩 Tech Stack (Reference)

| Layer | Technology |
|-------|-----------|
| ASR | IndicConformer, Vak (open-weight) |
| NLP | IndicBERT, MuRIL, Bhasha-Abhijnaanam |
| Vision | YOLOv8 (custom-trained on infrastructure defects) |
| Backend | Python (FastAPI), PostgreSQL + PostGIS |
| Frontend | React Native (mobile), React (web) |
| AI Orchestration | LangChain, custom pipelines |
| Data Integration | Apache Kafka, Debezium, REST/GraphQL |
| Consent | DEPA / Account Aggregator framework |
| Deployment | Kubernetes, on-premise or MeghRaj cloud |

---

## 📁 Repository Structure

```
janvastu/
├── docker-compose.yml
├── backend/                # Core API (FastAPI + PostgreSQL/PostGIS)
├── ai-pipeline/            # ASR, NLU, vision, decision pipelines
├── decision-support/       # Gap ratio, demand intensity, recommender
├── channels/               # IVR, WhatsApp bot, mobile app, CSC terminal
├── frontend/               # Policymaker dashboard, public portal
├── integrations/           # PFMS, IIG, eSAKSHI, CPGRAMS, DEPA clients
├── infra/                  # Terraform, Helm, Kubernetes manifests
└── docs/                   # README, PRD, rules, architecture, consent flow
```

See `docs/PRD.md`, `docs/rules.md`, `docs/architecture.md`, and `docs/consent-flow.md` for full specifications.
