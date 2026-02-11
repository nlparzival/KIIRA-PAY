# Compliance Matrix & Requirements Mapping
**Project Aurelius - Legal-to-Code Translation**

> **Status:** Living Document  
> **Laatste Update:** 11 februari 2026  
> **Doel:** Map elke juridische requirement naar concrete implementatie

---

## 🎯 Executive Summary

**The Challenge:**
> "We operate in 27 countries, each with national + EU laws. How do we ensure every agent, every transaction, is compliant?"

**The Solution:**
> "We translate law into executable code. Compliance is not checked, it's enforced by the system architecture."

**Scope:**
- 12 EU regulations/directives
- 5 national laws (Netherlands as pilot)
- 200+ specific requirements
- 1:1 mapping to code modules

**Status:**

| Regulation | Compliance Status | Priority |
|------------|-------------------|----------|
| **AI Act** | 🟡 In Progress (60% complete) | CRITICAL |
| **GDPR** | 🟢 Compliant (design phase) | CRITICAL |
| **eIDAS 2.0** | 🟡 In Progress (awaiting QTSP) | CRITICAL |
| **Digital Euro** | 🟡 Awaiting ECB specs | CRITICAL |
| **DORA** | 🟡 In Progress (40% complete) | HIGH |
| **NIS2** | 🟡 In Progress (50% complete) | HIGH |
| **MiCA** | 🟢 N/A (we're not crypto) | MEDIUM |
| **PSD2/3** | 🔴 Not Started (pending DNB guidance) | HIGH |
| **CSRD** | 🟢 Architecture supports | MEDIUM |
| **AML/CTF** | 🟡 In Progress (30% complete) | HIGH |
| **Energy Law (NL)** | 🟡 In Progress (50% complete) | CRITICAL |
| **Data Act** | 🟢 Architecture supports | MEDIUM |

---

## 📋 Regulation 1: EU AI Act (Regulation 2024/1689)

### Classification: HIGH-RISK AI SYSTEM

**Why:**
- Article 6(2), Annex III: AI for "management of critical infrastructure" (energy grids)
- Article 6(2), Annex III: AI for "creditworthiness assessment" (if agents borrow)

**Consequence:**
- Must comply with all high-risk requirements (Articles 8-15)
- Annual audits
- Heavy fines for non-compliance (€15M or 3% global turnover)

---

### Requirements & Implementation

#### Article 9: Risk Management System

**Legal Text:**
> "Providers shall put in place a risk management system consisting of a continuous iterative process..."

**Requirements:**
1. Identify risks (known + foreseeable)
2. Estimate and evaluate risks
3. Evaluate other emerging risks
4. Adopt mitigation measures
5. Test and document

**Our Implementation:**

```
CODE MODULE: risk_management_system.rs

├── Risk Identification (risk_identifier.rs)
│   ├── Static Risks (pre-defined)
│   │   └── Example: "Agent exceeds debt limit"
│   ├── Dynamic Risks (learned from data)
│   │   └── Example: "Unusual trading pattern detected"
│   └── Output: Risk Registry (database)
│
├── Risk Evaluation (risk_evaluator.rs)
│   ├── Likelihood Estimation (Bayesian model)
│   ├── Impact Assessment (financial + safety + legal)
│   └── Risk Score: Likelihood × Impact
│
├── Risk Mitigation (mitigations/)
│   ├── Circuit Breakers (automatic shutoff)
│   ├── Velocity Limits (rate limiting)
│   ├── Anomaly Detection (ML-based)
│   └── Human Override (emergency stop)
│
└── Risk Monitoring (risk_monitor.rs)
    ├── Real-time Dashboards (Grafana)
    ├── Alerting (PagerDuty)
    └── Audit Logs (immutable, WORM storage)
```

**Artifact Generated:**
- `Risk_Management_Plan_v1.0.pdf` (updated quarterly)
- Submitted to AFM for review

**Status:** 🟡 60% complete (documentation in progress)

---

#### Article 10: Data Governance

**Legal Text:**
> "Training, validation and testing data sets shall be subject to data governance and management practices..."

**Requirements:**
1. Data quality (relevant, accurate, representative)
2. Bias detection and mitigation
3. Data lineage (where did data come from?)
4. GDPR compliance (consent, right to erasure)

**Our Implementation:**

```
CODE MODULE: data_governance.rs

├── Data Collection (collectors/)
│   ├── Energy Price Data (APX, EPEX)
│   ├── Grid Frequency Data (TenneT API)
│   ├── Weather Data (KNMI, Meteomatics)
│   └── Transaction Data (our own ledger)
│
├── Data Validation (validators/)
│   ├── Schema Check (JSON schema validation)
│   ├── Range Check (values within expected bounds)
│   ├── Freshness Check (data not stale)
│   └── Bias Check (distribution analysis)
│
├── Data Lineage (lineage_tracker.rs)
│   ├── Provenance (where from? when? by whom?)
│   ├── Transformations (what operations applied?)
│   └── Usage (which models trained on this data?)
│
└── Data Retention (retention_policy.rs)
    ├── GDPR Compliance (delete after 7 years)
    ├── Right to Erasure (manual deletion on request)
    └── Backup Policy (encrypted, multi-region)
```

**Artifact Generated:**
- `Data_Governance_Policy_v1.0.pdf`
- Data lineage dashboard (internal tool)

**Status:** 🟡 50% complete (bias detection not yet implemented)

---

#### Article 11: Technical Documentation

**Legal Text:**
> "Technical documentation shall be drawn up... and kept up to date."

**Requirements:**
1. System design (architecture diagrams)
2. Data flow diagrams
3. Algorithm description
4. Risk assessment results
5. Test results and validation

**Our Implementation:**

**Artifacts:**
- [✅] `VISIE.md` (system architecture)
- [✅] `ARCHITECTUUR.md` (technical details)
- [✅] `SECURITY.md` (security model)
- [🟡] `AI_ALGORITHM_DOCUMENTATION.md` (in progress)
- [🟡] `TEST_VALIDATION_REPORT.pdf` (in progress)

**Storage:**
- Git repository (versioned, immutable)
- Submitted to AFM portal (official record)

**Status:** 🟡 70% complete (algorithm docs pending)

---

#### Article 13: Transparency & Information to Users

**Legal Text:**
> "High-risk AI systems shall be designed to enable users to interpret the system's output..."

**Requirements:**
1. Users must understand why AI made a decision
2. Provide explanations (not just black box)
3. Log all decisions (audit trail)

**Our Implementation:**

```
CODE MODULE: explainability.rs

├── Decision Logger (decision_log.rs)
│   ├── Input: What data was used?
│   ├── Model: Which model/algorithm?
│   ├── Output: What decision was made?
│   ├── Rationale: Why? (e.g., "Price spread = €0.20/kWh")
│   └── Confidence: How certain? (e.g., 95%)
│
├── User Dashboard (web UI)
│   ├── Transaction History
│   ├── Explanation per Transaction
│   │   └── Example: "Sold 5 kWh at 6pm because grid price was €0.35 (high)"
│   └── Performance Metrics (revenue, savings)
│
└── Regulator API (read-only)
    ├── Audit Log Access (AFM can query all decisions)
    └── Aggregate Statistics (not individual users)
```

**Example User Interface:**

```
Transaction #12345

Date: 2026-02-11 18:32:15
Action: SELL 5 kWh to grid
Price: €0.35/kWh
Revenue: €1.75

Why?
✓ Grid price (€0.35) > threshold (€0.25)
✓ Battery SoC (85%) > minimum (20%)
✓ Grid frequency (49.92 Hz) within range
✓ Forecasted solar production low (clouds)

Confidence: 94%

[View Full Decision Tree]
```

**Status:** 🟢 Implemented (basic version)

---

#### Article 14: Human Oversight

**Legal Text:**
> "High-risk AI systems shall be designed to enable effective oversight by natural persons..."

**Requirements:**
1. Humans can intervene (override AI)
2. Humans understand AI outputs
3. Monitoring dashboards

**Our Implementation:**

```
HUMAN OVERRIDE MECHANISMS:

1. Mobile App (agent owner)
   ├── Pause Agent (immediate)
   ├── Set Manual Limits (override AI)
   ├── Emergency Stop (kill switch)
   └── Notification: "AI paused, awaiting your approval"

2. Web Dashboard (advanced users)
   ├── Real-time Monitoring
   ├── Manual Trading Mode (you decide, not AI)
   └── Audit Log Review

3. Regulatory Interface (AFM/DNB)
   ├── Emergency Shutdown (all agents in region)
   ├── Audit Access (read-only, no control)
   └── Incident Reporting
```

**Default Settings:**
- Basic Tier: AI fully autonomous (but owner can override anytime)
- Pro Tier: Optional "approve all trades > €50"
- Enterprise Tier: Full manual control available

**Status:** 🟢 Implemented

---

#### Article 15: Accuracy, Robustness, Cybersecurity

**Legal Text:**
> "High-risk AI systems shall achieve appropriate levels of accuracy, robustness and cybersecurity..."

**Requirements:**
1. Accuracy: Measured and documented
2. Robustness: Works in adverse conditions
3. Cybersecurity: Protected against attacks

**Our Implementation:**

**Accuracy Metrics:**
- Trading Performance: Measured weekly (actual vs. predicted profit)
- Target: >80% accuracy (8/10 trades profitable)
- Reporting: Shown in user dashboard

**Robustness Testing:**
```
TEST SCENARIOS:

1. Network Outage
   - Simulate: Disconnect from internet
   - Expected: Agent falls back to local mode
   - Pass Criteria: No safety violations

2. Sensor Failure
   - Simulate: Smart meter stops reporting
   - Expected: Agent pauses trading
   - Pass Criteria: No blind trading

3. Price Spike
   - Simulate: Grid price jumps to €1/kWh (10x normal)
   - Expected: Agent pauses, requests human approval
   - Pass Criteria: No reckless trading

4. Adversarial Input
   - Simulate: Fake price data (man-in-the-middle)
   - Expected: Signature verification fails, data rejected
   - Pass Criteria: No action on fake data
```

**Cybersecurity:**
- See `SECURITY.md` for full threat model
- Compliance: ISO 27001 (planned), SOC 2 Type II (Q4 2026)

**Status:** 🟡 60% complete (robustness testing ongoing)

---

### AI Act Summary

**Total Requirements:** 47 specific items (Articles 8-15)  
**Implemented:** 28 (60%)  
**In Progress:** 15 (32%)  
**Not Started:** 4 (8%)

**Timeline:**
- Q2 2026: 80% complete (documentation finalized)
- Q3 2026: 100% complete (external audit)
- Q4 2026: Submit to AFM for approval

---

## 📋 Regulation 2: GDPR (General Data Protection Regulation)

### Classification: ALL PROCESSING = GDPR SCOPE

**Why:**
- Energy consumption data = personal data (GDPR Article 4.1)
- Agent acts on behalf of person → Still personal data
- Even aggregated data can be re-identified

---

### Key Principles & Implementation

#### Article 5: Data Processing Principles

**Legal Text:**
> "Personal data shall be processed lawfully, fairly, and transparently..."

| Principle | Requirement | Our Implementation |
|-----------|-------------|-------------------|
| **Lawfulness** | Legal basis (consent, contract, etc.) | Consent (opt-in), Contract (service agreement) |
| **Purpose Limitation** | Use data only for stated purpose | Energy optimization ONLY (never sold) |
| **Data Minimization** | Collect only what's necessary | Aggregate data (kWh totals, not appliance-level) |
| **Accuracy** | Keep data accurate and up-to-date | Smart meter = real-time, accurate |
| **Storage Limitation** | Don't keep forever | 7 years (legal requirement), then delete |
| **Integrity & Confidentiality** | Protect data | Encryption (at rest + in transit), HSM |
| **Accountability** | Prove compliance | Audit logs, DPIA, DPO |

---

#### Article 6: Legal Basis

**Our Legal Bases:**

1. **Consent (Article 6.1.a):** User explicitly opts in
   - Consent form: Clear, specific, informed
   - Granular: Separate consent for each processing purpose
   - Revocable: User can withdraw anytime (delete account)

2. **Contract (Article 6.1.b):** Necessary for service delivery
   - We need energy data to provide optimization service
   - Can't optimize without knowing consumption patterns

3. **Legitimate Interest (Article 6.1.f):** For anonymized research
   - Example: "Aggregated energy trends for EU Green Deal reporting"
   - Balancing test: Our interest vs. user rights (documented)

---

#### Article 13-14: Information to Data Subjects

**Required Information:**
1. Who we are (Aurelius BV)
2. Why we process (energy optimization)
3. Legal basis (consent + contract)
4. How long we keep data (7 years)
5. User rights (access, erasure, portability)
6. How to complain (Dutch DPA: autoriteitpersoonsgegevens.nl)

**Our Implementation:**
- Privacy Policy (clear, simple language)
- Consent screen (checkbox + link to policy)
- Dashboard: "Your Data & Privacy" section

---

#### Article 15-22: Data Subject Rights

| Right | Implementation |
|-------|----------------|
| **Access (Art. 15)** | Dashboard: "Download My Data" (JSON export) |
| **Rectification (Art. 16)** | Edit profile, update preferences |
| **Erasure (Art. 17)** | "Delete Account" button (permanent) |
| **Portability (Art. 20)** | Export in machine-readable format (JSON, CSV) |
| **Object (Art. 21)** | Opt-out of specific processing (e.g., analytics) |
| **Automated Decision (Art. 22)** | Right to human review (contact support) |

**Response Time:** 30 days (GDPR requirement)

---

#### Article 25: Privacy by Design

**Principle:**
> "Design systems with privacy in mind from the start, not as an afterthought."

**Our Approach:**

```
PRIVACY BY DESIGN FEATURES:

1. Data Minimization (Code-Level)
   - Don't log more than necessary
   - Example: Log "Transaction: 5 kWh sold"
            NOT "User at home, fridge on, TV on, etc."

2. Pseudonymization
   - User ID = UUID (not name)
   - Agent ID = EUID (European Unique Identifier, not personal)
   - Transactions linked to agents, not humans

3. Encryption by Default
   - All data encrypted at rest (AES-256)
   - All data encrypted in transit (TLS 1.3)
   - Keys in HSM (not on servers)

4. Access Controls
   - Role-based (RBAC): Developers can't access production data
   - Need-to-know: Only authorized personnel

5. Anonymization for Analytics
   - Before aggregating: Remove identifiers
   - K-anonymity: ≥100 users in each group (can't single out)
```

---

#### Article 35: Data Protection Impact Assessment (DPIA)

**When Required:**
- High-risk processing (profiling, automated decisions)
- We qualify: AI making financial decisions

**Our DPIA (Summary):**

**1. Description of Processing**
- Purpose: Energy trading optimization
- Data: Energy consumption, trading transactions, battery state
- Technology: AI/ML (reinforcement learning)

**2. Necessity & Proportionality**
- Why needed: Can't optimize without data
- Alternatives considered: Manual control (less effective)
- Proportionality: Minimal data collected

**3. Risks to Rights & Freedoms**
- Risk 1: Data breach → Financial loss
  - Mitigation: Encryption, HSM, monitoring
- Risk 2: Profiling → Discrimination
  - Mitigation: No human profiling (only energy patterns)
- Risk 3: Unauthorized access → Privacy violation
  - Mitigation: Access controls, audit logs

**4. Consultation**
- Data Protection Officer (DPO): Consulted ✅
- Dutch DPA: Notified (high-risk processing)

**Status:** 🟢 Completed, approved by DPO

---

### GDPR Summary

**Compliance Status:** 🟢 90% (design phase)  
**Remaining:** DPO appointment (Q2 2026), ongoing monitoring

---

## 📋 Regulation 3: eIDAS 2.0 (Electronic Identification)

### Classification: QUALIFIED TRUST SERVICES REQUIRED

**Why:**
- Agents sign transactions (legal standing)
- Must use Qualified Signature (QES) under eIDAS
- Otherwise: Signatures not legally binding across EU

---

### Requirements & Implementation

#### Article 25: Qualified Electronic Signatures

**Legal Text:**
> "A qualified electronic signature shall have the equivalent legal effect of a handwritten signature."

**Requirements:**
1. Signature created by **QSCD** (Qualified Signature Creation Device)
   - Hardware device (HSM qualifies)
   - Must be eIDAS certified
2. Certificate issued by **QTSP** (Qualified Trust Service Provider)
   - Government-approved (e.g., KPN, Digidentity)
3. Unique link to signatory (agent = legal entity via EUinc)

**Our Implementation:**

```
SIGNATURE FLOW:

1. Agent Onboarding
   ├── Create EUinc entity (legal identity)
   ├── Generate key pair in HSM (QSCD)
   ├── Submit CSR to QTSP (e.g., Digidentity)
   └── Receive certificate (X.509, eIDAS compliant)

2. Transaction Signing
   ├── Agent decides to trade
   ├── Gateway prepares transaction data
   ├── Hash data (SHA-256)
   ├── Send hash to HSM
   ├── HSM signs with agent's private key (never leaves HSM)
   ├── Return signature (EdDSA, 64 bytes)
   └── Attach signature + certificate to transaction

3. Verification (by recipient or regulator)
   ├── Extract signature + certificate from transaction
   ├── Verify certificate (check QTSP signature)
   ├── Verify signature (public key from certificate)
   ├── Check revocation (OCSP or CRL)
   └── Result: VALID or INVALID
```

**Status:** 🟡 Awaiting QTSP partnership (Digidentity in talks)

---

#### Article 3: European Digital Identity Wallet

**What:**
- EU mandates every citizen/company gets a digital wallet (by 2026)
- Wallet contains: ID, driver's license, certificates, payment credentials

**For Aurelius:**
- Each agent = wallet (via EUinc)
- Wallet contains: Agent ID, signing certificate, Digital Euro credentials

**Integration:**
- eIDAS 2.0 API (standard protocol, ARF - Architecture Reference Framework)
- Wallet providers: National (DigiD in NL) + commercial (Digidentity, KPN)

**Status:** 🟡 Monitoring eIDAS 2.0 implementation (Q3 2026 expected)

---

## 📋 Regulation 4: DORA (Digital Operational Resilience Act)

### Classification: FINANCIAL ENTITY (if we get payment license)

**Why:**
- If we're classified as Payment Institution (PSD3) → DORA applies
- DORA = operational resilience for financial services

---

### Key Requirements & Implementation

#### Article 6-7: ICT Risk Management

**Requirements:**
1. Risk management framework
2. ICT systems protected (confidentiality, integrity, availability)
3. Incident detection and response
4. Business continuity planning
5. Testing (annual penetration tests)

**Our Implementation:**

```
ICT RISK MANAGEMENT:

1. Risk Register
   ├── Identified Risks (threat model)
   ├── Likelihood + Impact
   └── Mitigation Measures

2. Security Controls
   ├── Multi-cloud (no single point of failure)
   ├── HSM (keys protected)
   ├── Encryption (data at rest + in transit)
   └── Monitoring (24/7, Prometheus + Grafana)

3. Incident Response
   ├── Playbooks (documented procedures)
   ├── Drills (quarterly tabletop exercises)
   └── Recovery (RTO = 2 hours, RPO = 15 minutes)

4. Business Continuity
   ├── Disaster Recovery Plan
   ├── Backup Data Centers (Frankfurt, Milan)
   └── Manual Fallback (if all systems down)

5. Testing
   ├── Penetration Tests (quarterly)
   ├── Disaster Recovery Drills (annual)
   └── Third-Party Audits (SOC 2, ISO 27001)
```

**Status:** 🟡 50% complete (BCP documentation pending)

---

#### Article 28: Reporting to Authorities

**Requirements:**
- Report major incidents to DNB within 4 hours (initial), 72 hours (full report)

**Our Implementation:**
- Automated alerts → PagerDuty → On-call engineer
- Template reports (pre-filled, submit via DNB portal)
- Legal review (before submitting final report)

**Status:** 🟢 Implemented (templates ready)

---

## 📋 Regulation 5: Energy Law (Netherlands)

### Elektriciteitswet 1998 + EU Directives

#### Article 31a: Net Metering (Saldering)

**Legal Text:**
> "Prosumers may offset consumption with self-generated electricity"

**Relevance:**
- Agents trading surplus solar = prosumer activity
- Legally allowed under net metering

**Our Implementation:**
- Agents registered as prosumers (via energy supplier)
- Transactions logged (for annual settlement)

**Status:** 🟢 Compliant

---

#### EU Directive 2019/944: Right to Participate in Markets

**Article 15: Active Customers**

**Legal Text:**
> "Active customers shall be able to participate in all electricity markets"

**Relevance:**
- Agents = active customers (automated, but still customers)
- Must have access to day-ahead, intraday, balancing markets

**Our Implementation:**
- Register agents with TenneT (Market Party ID)
- Use ENTSO-E protocols (standard APIs)

**Status:** 🟡 TenneT registration pending (pilot phase)

---

## 📋 Master Compliance Checklist

### Critical Path (Must Have for Launch)

- [ ] **AI Act:** Risk management system documented
- [ ] **AI Act:** Technical documentation complete
- [ ] **GDPR:** DPIA approved by DPO
- [ ] **GDPR:** Privacy policy published
- [ ] **eIDAS:** QTSP partnership signed
- [ ] **eIDAS:** HSM eIDAS-certified
- [ ] **Energy Law:** TenneT registration submitted
- [ ] **Energy Law:** Prosumer registration (via supplier)

### High Priority (Needed for Scale)

- [ ] **DORA:** Business continuity plan documented
- [ ] **DORA:** Disaster recovery tested
- [ ] **NIS2:** Cybersecurity measures implemented
- [ ] **PSD3:** DNB guidance clarified (are we payment institution?)
- [ ] **AML/CTF:** KYC procedures documented

### Medium Priority (Good to Have)

- [ ] **CSRD:** ESG reporting dashboard
- [ ] **Data Act:** Data portability tested
- [ ] **ISO 27001:** Certification achieved
- [ ] **SOC 2 Type II:** Audit completed

---

## 🎯 Compliance Roadmap

### Q1 2026
- ✅ GDPR: DPIA completed
- 🟡 AI Act: Documentation 60% complete
- 🟡 eIDAS: QTSP negotiations ongoing

### Q2 2026
- [ ] AI Act: 100% documentation
- [ ] eIDAS: QTSP contract signed
- [ ] Energy Law: TenneT registration approved

### Q3 2026
- [ ] AI Act: External audit (submit to AFM)
- [ ] DORA: Business continuity plan approved
- [ ] SOC 2: Type II audit initiated

### Q4 2026
- [ ] All critical compliance items: 100%
- [ ] Regulatory approvals: DNB, AFM, TenneT
- [ ] Ready for scale (10k+ agents)

---

## 📞 Regulatory Contacts

| Authority | Contact | Topic | Status |
|-----------|---------|-------|--------|
| **DNB** | innovationhub@dnb.nl | Payment license, DORA | 🔴 Not contacted |
| **AFM** | toezicht@afm.nl | AI Act, MiCA | 🔴 Not contacted |
| **Dutch DPA** | info@autoriteitpersoonsgegevens.nl | GDPR | 🟢 DPIA submitted |
| **TenneT** | balancing@tennet.eu | Grid access | 🟡 Initial contact |
| **Digidentity** | sales@digidentity.eu | eIDAS QTSP | 🟡 Negotiations |

---

## ✅ Next Steps

1. [ ] Finalize AI Act documentation (Q1 2026)
2. [ ] Sign QTSP contract (Q2 2026)
3. [ ] Submit DNB Innovation Hub application (Q1 2026)
4. [ ] Complete DORA compliance (Q3 2026)
5. [ ] External security audit (Q3 2026)

---

**Remember: Compliance is not a checklist, it's a culture. We build it in, not bolt it on.**

