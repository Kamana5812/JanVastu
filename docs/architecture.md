# JanVastu — System Architecture

**Version**: 1.0
**Last Updated**: 2025

---

## 1. Architectural Principles

1. **Digital Public Good by Design** — Open-source, interoperable, privacy-preserving
2. **Voice-First** — Primary interface for low-literacy populations
3. **Offline-Capable** — Functions without continuous connectivity
4. **Federated** — Queries distributed data sources; doesn't centralize sensitive data
5. **Explainable** — Every recommendation has auditable attribution
6. **Sovereign** — On-premise deployable; no mandatory foreign API dependencies
7. **DPDP-Compliant** — Anonymization at ingestion; consent-driven

---

## 2. High-Level Architecture

The platform is organized into three primary layers plus an Accountability Module (see `README.md`):

1. Collection Layer
2. AI Processing Layer
3. Decision Support Layer
4. Accountability Module (cross-cutting, reads from Data Fusion Layer)

A Data Fusion Layer sits between AI Processing and Decision Support, storing demand, asset, and accountability data and streaming changes via Kafka/Debezium.

---

## 3. Component Details

### 3.1 Collection Layer

**IVR Gateway**
- Asterisk/FreeSWITCH for call handling
- IndicConformer ASR for real-time transcription
- IVR flow in 22 languages
- Fallback to human operator for low-confidence

**WhatsApp/SMS Chatbot**
- WhatsApp Business API (Meta) or Gupshup
- SMS fallback via SMS gateway
- Supports voice messages, text, images, video
- Multilingual NLU

**Mobile App (Citizen)**
- React Native (iOS + Android)
- Offline-first (SQLite + sync queue)
- Camera integration with geo-tagging
- Voice recording with compression
- Multilingual UI (22 languages)

**Mobile App (Volunteer Mode)**
- Same app with elevated permissions
- GPS verification of collection point
- Household-level data collection forms
- Batch sync when online

**CSC Terminal**
- Web-based interface for CSC operators
- Assisted input for citizens without devices
- Aadhaar-based optional verification
- Receipt printing with complaint ID

---

### 3.2 AI Processing Layer

**ASR Module**
- IndicConformer models (AI4Bharat) for 22 languages
- Vak open-weight models for 55 languages (extended)
- Code-switching support (Hinglish, Tanglish, Banglish)
- Confidence scoring with human-in-the-loop fallback

**Language Identification**
- FastText-based classifier for language + dialect
- Handles code-switched inputs

**Intent Classification**
- Fine-tuned IndicBERT/MuRIL
- Categories: Road, Water, Health, Education, Electricity, Sanitation, Housing, Other
- Multi-label support (a feedback can span categories)

**Named Entity Recognition**
- Place name extraction (village, block, district)
- Landmark extraction
- Custom gazetteer for Indian administrative units

**Geo-coding**
- Reverse geocoding via OpenStreetMap + Bhuvan (ISRO)
- Fallback to user-provided location
- Confidence scoring

**Image Classification**
- YOLOv8 custom-trained on infrastructure defects
- Categories: Pothole, Broken bridge, Non-functional pump, Damaged school, etc.
- Severity estimation

**Video Summarization**
- Frame sampling + classification
- Duration/resolution validation
- Content summary for review

**Deduplication & Anomaly Detection**
- MinHash LSH for near-duplicate detection
- Submission pattern anomaly detection
- GPS plausibility checks

---

### 3.3 Data Fusion Layer

**Demand Data Store**
- PostgreSQL + PostGIS
- Feedback items with geo-coordinates
- Media references (S3-compatible object store)
- Demand Intensity Scores

**Asset Data Store**
- Project locations from IIG, eSAKSHI, PMGSY GIS
- Infrastructure Stock Indices from departmental datasets
- Spatial join capability

**Accountability Data Store**
- Federated queries to PFMS, IIG, eSAKSHI
- Cached contractor/official/cost records
- Public/private field segregation

**Streaming & CDC**
- Kafka for real-time ingestion
- Debezium for change data capture from source systems
- Redis for hot cache

---

### 3.4 Decision Support Layer

**Demand-Supply Gap Analysis**
- Computes Gap Ratio per geographic unit
- Formula: Demand Intensity / (Infrastructure Stock + Planned Investment)
- Weights by population vulnerability

**Priority Project Recommender**
- Ranks geographic units by Gap Ratio
- Suggests project types based on dominant demand category
- Explainable AI: every recommendation includes attribution

**Contractor Performance Dashboard**
- Aggregates citizen complaints by contractor
- Tracks resolution time
- Flags repeat offenders

**Agency Responsiveness Tracker**
- Measures time-to-resolution by department
- Compares across districts/states
- Public scorecard

**Asset Health Monitor**
- Links citizen media to specific assets
- Tracks condition over time
- Predicts maintenance needs

**Feedback-to-Resolution Tracker**
- Public ledger of feedback → action → outcome
- Prevents "open-washing"

---

### 3.5 Output Channels

**Policymaker Dashboard**
- Web-based (React)
- Role-based access (District, State, National)
- Demand heatmaps, Gap Ratios, recommendations
- Export to PDF/Excel for planning meetings

**Public Transparency Portal**
- Public-facing website
- Search projects by location
- View contractor, cost, timeline, officials
- Track complaint status

**Grievance Redressal Integration**
- CPGRAMS API integration
- Rajmargyatra (NHAI) integration
- MeriSadak (PMGSY) integration
- State e-District portals

---

## 4. Data Flow

### 4.1 Citizen Feedback Flow

See `consent-flow.md` for the full consent capture sequence that precedes every feedback submission. At a high level: citizen contact → consent → feedback capture → AI enrichment (language, intent, geo, media classification) → dedup/anomaly check → write to Demand Data Store → available to Decision Support Layer.

---

## 5. Deployment Architecture

### 5.1 On-Premise (Recommended for Sovereignty)

- Kubernetes cluster (MeghRaj cloud or NIC)
- PostgreSQL with streaming replication
- MinIO for object storage
- Kafka cluster (3+ brokers)
- GPU nodes for ASR/vision inference
- Prometheus + Grafana for monitoring
- ELK stack for logs

### 5.2 Hybrid (For Scale)

- Core processing on-premise (sovereignty)
- CDN for static assets
- Read replicas in regional data centers
- Optional cloud burst for batch processing

### 5.3 Field Deployment

- Mobile app works fully offline
- Volunteer mode syncs via 2G/3G when available
- IVR gateways in regional telecom circles
- CSC terminals on existing NIC network

---

## 6. Security Architecture

| Layer | Control |
|-------|---------|
| Network | VPC isolation, WAF, DDoS protection |
| Identity | OAuth2/OIDC, MFA for officials, Aadhaar optional for citizens |
| Data at rest | AES-256 encryption |
| Data in transit | TLS 1.3 |
| Consent | DEPA/Account Aggregator framework |
| Anonymization | Ingestion-time PII stripping |
| Audit | Immutable logs (append-only) |
| Access | RBAC with least privilege |
| Media | Virus scanning, format validation, size limits |

---

## 7. Integration Points

| System | Purpose | Protocol | Status |
|--------|---------|----------|--------|
| PFMS | Fund flow data | REST API | Pending MoU |
| IIG | NIP project data | REST API | Pending MoU |
| eSAKSHI | MPLADS data | REST API | Pending MoU |
| CPGRAMS | Grievance routing | REST API | Available |
| Rajmargyatra | Highway complaints | Deep link | Available |
| MeriSadak | PMGSY complaints | Deep link | Available |
| DEPA/AA | Consent management | API | Available |
| Bhuvan (ISRO) | Geospatial data | WMS/WFS | Available |
| Census | Demographic data | Bulk import | Available |
| CSC | Terminal access | NIC network | Available |

---

## 8. Scalability Strategy

| Dimension | Strategy |
|-----------|----------|
| Ingestion | Kafka partitioning by geography |
| ASR | GPU pool with autoscaling |
| Storage | Sharded PostgreSQL + object store |
| Analytics | Pre-computed aggregates + materialized views |
| API | Horizontal pod autoscaling |
| Media | CDN for public assets; lifecycle policies |
| Geographic | Regional deployments with central aggregation |

---

## 9. Disaster Recovery

- RPO: 15 minutes
- RTO: 4 hours
- Multi-region replication
- Daily encrypted backups
- Quarterly DR drills

---

## 10. Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| ASR | IndicConformer, Vak |
| NLP | IndicBERT, MuRIL, FastText |
| Vision | YOLOv8 |
| Backend | Python (FastAPI), Node.js (BFF) |
| Database | PostgreSQL + PostGIS, Redis |
| Streaming | Apache Kafka, Debezium |
| Object Store | MinIO / S3-compatible |
| Frontend | React Native, React |
| API Gateway | Kong / Envoy |
| Orchestration | Kubernetes |
| Monitoring | Prometheus, Grafana, ELK |
| CI/CD | GitLab CI / GitHub Actions |
| IaC | Terraform, Helm |
