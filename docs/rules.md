> Earlier proposal. The current hackathon specification is [the root PRD](../PRD.md). See [implementation status](../IMPLEMENTATION_SUMMARY.md) for delivered scope and external dependencies.

# JanVastu — Rules, Standards & Governance

**Version**: 1.0
**Last Updated**: 2025

---

## 1. Core Principles

1. **Digital Public Good** — Open-source, interoperable, privacy-preserving
2. **Do No Harm by Design** — Anticipate and mitigate adverse impacts
3. **Citizen Sovereignty** — Citizens own their data; consent is foundational
4. **Explainability** — No black-box decisions affecting citizens
5. **Inclusivity** — Voice-first, multilingual, offline-capable
6. **Transparency** — Public audit trail; open algorithms
7. **Accountability** — Every recommendation traceable to evidence

---

## 2. Coding Standards

### 2.1 General
- **Languages**: Python 3.11+, TypeScript 5+, Kotlin/Swift (mobile)
- **Style**: PEP 8 (Python), ESLint + Prettier (JS/TS)
- **Formatting**: Black (Python), Prettier (TS)
- **Linting**: Ruff (Python), ESLint (TS)
- **Type Checking**: mypy (Python), TypeScript strict mode

### 2.2 Python
```python
# Use type hints everywhere
def compute_gap_ratio(
    demand_score: float,
    infra_stock: float,
    planned_investment: float,
) -> float:
    """Compute Demand-Supply Gap Ratio."""
    if infra_stock + planned_investment == 0:
        return float("inf")
    return demand_score / (infra_stock + planned_investment)
```
