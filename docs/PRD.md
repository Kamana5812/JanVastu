# JanVastu — Product Requirements Document (PRD)

**Version**: 1.0
**Status**: Draft
**Last Updated**: 2025
**Owner**: JanVastu Core Team

---

## 1. Executive Summary

JanVastu is a multilingual, AI-powered Digital Public Good that aggregates citizen development requests across India and aligns them with national infrastructure planning. It surfaces demand hotspots, recommends high-priority projects, and provides end-to-end accountability by exposing project-level details (contractor, cost, timeline, responsible officials).

---

## 2. Problem Statement

### 2.1 Fragmented Citizen Feedback
Citizen development requests are scattered across:
- MPLADS recommendations (₹5 crore/MP/year)
- e-District grievance portals
- CPGRAMS
- State PWD complaint systems
- CSC service touchpoints (5 lakh+ centers)

No unified system captures, aggregates, or spatializes this demand.

### 2.2 Top-Down Infrastructure Planning
The National Infrastructure Pipeline (NIP) contains 9,000+ projects worth ₹160+ trillion, but project identification is driven by central ministries and state governments — not citizen demand.

### 2.3 No Accountability Layer
Once built, citizens cannot find:
- Who built a project (contractor)
- Who manages it (officials, HODs)
- How much it cost
- When it was supposed to be completed
- Whether it's functioning

### 2.4 Exclusion of Low-Literacy, Non-Smartphone Populations
Existing digital feedback systems assume text literacy and smartphone access, systematically excluding the populations most in need of infrastructure.

---

## 3. Goals & Objectives

### 3.1 Primary Goals
1. Aggregate citizen development demand across voice, text, photo, video, and messaging channels
2. Process feedback using multilingual AI (22+ Indian languages)
3. Compute Demand-Supply Gap Ratios at village/ward/block level
4. Recommend priority projects to policymakers with explainable AI
5. Provide project accountability details (contractor, cost, timeline, officials)
6. Comply with DPDP Act 2023 and DPG Standard

### 3.2 Success Metrics
| Metric | Target (Year 1) | Target (Year 3) |
|--------|----------------|----------------|
| Languages supported | 5 | 22 |
| States covered | 3 | 28 |
| Citizens reached | 1 million | 50 million |
| Feedback items processed | 500,000 | 50 million |
| Priority projects recommended | 500 | 10,000 |
| Accountability records published | 1,000 | 100,000 |
| ASR accuracy (top 5 languages) | ≥85% WER | ≥92% WER |

---

## 4. User Personas

### 4.1 Citizen — Ramesh (Rural, Low Literacy)
- 45, farmer, Bihar, owns a basic phone
- Cannot read/write fluently but can speak Hindi and Bhojpuri
- Uses IVR to report broken canal, uploads photo via volunteer

### 4.2 Citizen — Priya (Urban, Digital Native)
- 28, software engineer, Bengaluru
- Reports potholes via WhatsApp with geo-tagged photo
- Wants to see contractor details and hold officials accountable

### 4.3 Volunteer — Anjali (PFSMS-style Field Worker)
- 22, community mobilizer, Maharashtra
- Uses offline mobile app to collect household feedback
- Syncs when connectivity available

### 4.4 Policymaker — District Collector
- Needs demand hotspot data for MPLADS recommendations
- Needs contractor performance data for oversight
- Requires explainable AI outputs

### 4.5 National Planner — NITI Aayog Official
- Needs aggregated demand signals for NIP prioritization
- Requires integration with existing planning workflows
- Needs audit trail for accountability

---

## 5. Functional Requirements

### 5.1 Collection Layer

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | Support IVR voice calls in 22 Indian languages | P0 |
| FR-1.2 | Support WhatsApp/SMS chatbot with voice & text | P0 |
| FR-1.3 | Mobile app with offline capture & auto-sync | P0 |
| FR-1.4 | CSC terminal interface for assisted input | P1 |
| FR-1.5 | Volunteer mode with GPS-verified collection | P0 |
| FR-1.6 | Photo upload with auto geo-tag & timestamp | P0 |
| FR-1.7 | Video upload (≤60s) with compression | P0 |
| FR-1.8 | Voice annotation in local language | P0 |
| FR-1.9 | Anonymization at point of ingestion | P0 |
| FR-1.10 | Consent capture (DPDP-compliant) | P0 |

### 5.2 AI Processing Layer

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | ASR for 22 Indian languages (IndicConformer) | P0 |
| FR-2.2 | Automatic language identification | P0 |
| FR-2.3 | Intent classification (road/water/health/etc.) | P0 |
| FR-2.4 | Named Entity Recognition for place names | P0 |
| FR-2.5 | Reverse geocoding to lat/long | P0 |
| FR-2.6 | Image classification (pothole/broken pump/etc.) | P0 |
| FR-2.7 | Video content summarization | P1 |
| FR-2.8 | Deduplication & anomaly detection | P0 |
| FR-2.9 | Urgency classification | P1 |
| FR-2.10 | Code-switching support (Hinglish, Tanglish) | P0 |

### 5.3 Decision Support Layer

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | Demand Intensity Score computation | P0 |
| FR-3.2 | Infrastructure Stock Index integration | P0 |
| FR-3.3 | Demand-Supply Gap Ratio calculation | P0 |
| FR-3.4 | Priority project recommendations | P0 |
| FR-3.5 | Explainable AI attribution | P0 |
| FR-3.6 | Demand hotspot heatmaps | P0 |
| FR-3.7 | Contractor performance dashboards | P1 |
| FR-3.8 | Agency responsiveness tracking | P1 |
| FR-3.9 | Integration with NIP, MPLADS, PMGSY | P0 |
| FR-3.10 | Public transparency portal | P0 |

### 5.4 Accountability Module

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-4.1 | Project lookup by GPS coordinates | P0 |
| FR-4.2 | Display contractor/vendor name | P0 |
| FR-4.3 | Display sanctioned & actual cost | P0 |
| FR-4.4 | Display project timeline (planned/actual) | P0 |
| FR-4.5 | Display responsible officials (designation + office contact) | P0 |
| FR-4.6 | Display HOD and department chain | P1 |
| FR-4.7 | Integration with PFMS for fund flow | P1 |
| FR-4.8 | Integration with IIG for NIP projects | P0 |
| FR-4.9 | Integration with eSAKSHI for MPLADS | P0 |
| FR-4.10 | Citizen media evidence linked to asset | P0 |

### 5.5 Governance & Compliance

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-5.1 | DPDP Act 2023 compliance (consent, erasure, audit) | P0 |
| FR-5.2 | DPG Standard alignment (9 indicators) | P0 |
| FR-5.3 | DEPA/Account Aggregator integration | P1 |
| FR-5.4 | Open-source licensing (Apache 2.0) | P0 |
| FR-5.5 | On-premise deployment option | P0 |
| FR-5.6 | Independent data auditor appointment | P0 |
| FR-5.7 | Public audit trail | P0 |
| FR-5.8 | Grievance integration (CPGRAMS, Rajmargyatra, MeriSadak) | P0 |

---

## 6. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Scalability** | Support 50M+ feedback items; horizontal scaling via Kubernetes |
| **Availability** | 99.5% uptime; offline-first mobile app |
| **Latency** | ASR processing <5s per 30s audio; API responses <500ms |
| **Security** | End-to-end encryption; AES-256 at rest; TLS 1.3 in transit |
| **Privacy** | Anonymization at ingestion; no PII retention beyond consent scope |
| **Accessibility** | WCAG 2.1 AA; voice-first for low-literacy |
| **Localization** | 22 languages; RTL support for Urdu |
| **Interoperability** | Open APIs; DEPA-compliant consent; DPG Standard |
| **Auditability** | Immutable logs; explainable AI outputs |
| **Portability** | On-premise, MeghRaj cloud, or hybrid |

---

## 7. Out of Scope (v1.0)

- Direct fund disbursement
- Project execution monitoring (only feedback & accountability)
- Real-time video streaming
- Private sector infrastructure feedback
- International deployment (planned for v3.0)

---

## 8. Dependencies

| Dependency | Owner | Status |
|-----------|-------|--------|
| PFMS data-sharing agreement | CGA | Pending |
| IIG API access | DEA | Pending |
| eSAKSHI integration | Ministry of Statistics | Pending |
| DEPA integration | Sahamati | Available |
| CSC network access | MeitY | Available |
| IndicConformer models | AI4Bharat | Available |
| Vak open-weight models | Shunya Labs | Available |

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Elite capture | Weight by vulnerability index; CSC outreach |
| Manipulation | Anomaly detection; GPS verification |
| ASR performance gaps | Phase language rollout; transparent reporting |
| Political resistance | Position as decision-support, not replacement |
| Data silos | Federated architecture; MoUs with ministries |
| Privacy concerns | Anonymization; DPDP compliance; independent audit |

---

## 10. Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Lead | | | |
| Technical Lead | | | |
| Governance Lead | | | |
| DPG Advisor | | | |
