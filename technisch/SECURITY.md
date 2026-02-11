# Security Architecture & Threat Model
**Project Aurelius - Defense in Depth**

> **Status:** Living Document  
> **Laatste Update:** 11 februari 2026  
> **Doel:** Complete security model, threat analysis, mitigations

---

## 🎯 Executive Summary

**Security Posture:**
> "We assume everything will be attacked. We design so attacks fail, not so they're unlikely."

**Core Principles:**

1. **Zero Trust:** Never trust, always verify
2. **Defense in Depth:** Multiple independent layers
3. **Fail Secure:** When in doubt, shut down safely
4. **Cryptographic Proof:** Math, not promises
5. **Auditability:** Every action leaves immutable trace

**Threat Model:**

| Threat Level | Actor | Capability | Mitigation |
|--------------|-------|------------|------------|
| **CRITICAL** | Nation-state | Unlimited resources, zero-days | HSM physical security, air gaps |
| **HIGH** | Organized crime | Ransomware, DDoS, social engineering | Incident response, backups, training |
| **MEDIUM** | Hacktivist | Public exploits, defacement | Patching, WAF, monitoring |
| **LOW** | Script kiddie | Automated tools | Basic hardening, rate limiting |

**Investment:** 15% of engineering budget goes to security (vs. 5% industry average)

---

## 🔐 Cryptographic Foundation (eIDAS 2.0)

### What is eIDAS 2.0?

**eIDAS = electronic IDentification, Authentication and trust Services**

**eIDAS 1.0 (2016):**
- Focus: Cross-border recognition of e-signatures
- Use case: Sign PDF documents legally across EU

**eIDAS 2.0 (2024, fully enforced 2026):**
- Adds: **European Digital Identity Wallets (EUDIW)**
- Use case: Every EU citizen/company gets a cryptographic wallet
- Think: "Passport + driver's license + bank card" in one app

**For Aurelius:**
- Each agent gets an eIDAS wallet (legal identity)
- Wallet contains private keys (stored in HSM)
- Every transaction signed = legally binding across all 27 EU countries

---

### Key Types & Hierarchy

```
[Root of Trust: Hardware Security Module (HSM)]
│
├── Master Key (never leaves HSM)
│   ├── Rotation: Every 90 days
│   ├── Backup: Encrypted, offline, geographically distributed
│   └── Access: Requires 3-of-5 ceremony (Shamir Secret Sharing)
│
├── Agent Signing Keys (per-agent, ephemeral)
│   ├── Lifetime: 30 days (auto-rotation)
│   ├── Algorithm: EdDSA (Ed25519) - fast, quantum-resistant ready
│   ├── Usage: Sign transactions, mandates, state updates
│   └── Revocation: Instant (publish to CRL, OCSP)
│
├── Communication Keys (per-session, short-lived)
│   ├── Lifetime: 1 hour (PFS - Perfect Forward Secrecy)
│   ├── Algorithm: X25519 (ECDH) + ChaCha20-Poly1305 (AEAD)
│   └── Usage: Encrypt data in transit
│
└── Backup/Recovery Keys (cold storage)
    ├── Lifetime: Indefinite (disaster recovery only)
    ├── Storage: Paper wallets + Shamir shards (3-of-5)
    └── Location: Bank vaults (3 countries)
```

---

### Signature Scheme (EdDSA)

**Why EdDSA (Ed25519) over RSA or ECDSA?**

| Feature | RSA-2048 | ECDSA P-256 | EdDSA (Ed25519) |
|---------|----------|-------------|-----------------|
| **Security** | 112-bit | 128-bit | 128-bit |
| **Key Size** | 2048 bits | 256 bits | 256 bits |
| **Signature Size** | 256 bytes | 64 bytes | **64 bytes** |
| **Sign Speed** | Slow | Medium | **Fast (71k/sec)** |
| **Verify Speed** | Slow | Medium | **Fast (20k/sec)** |
| **Complexity** | High (padding, RNG) | Medium (nonce) | **Low (deterministic)** |
| **Quantum Resistance** | ❌ (Shor's algorithm) | ❌ (Shor's) | ⚠️ (Better, not immune) |

**Decision:** Ed25519 for now, migrate to post-quantum (ML-DSA, SLH-DSA) when eIDAS mandates it (expected 2028-2030)

---

### Encryption Scheme (ChaCha20-Poly1305)

**For data in transit:**

**Why ChaCha20 over AES?**

| Feature | AES-256-GCM | ChaCha20-Poly1305 |
|---------|-------------|-------------------|
| **Security** | 256-bit | 256-bit |
| **Speed (software)** | Medium | **Fast (3x on ARM)** |
| **Speed (hardware)** | Fast (AES-NI) | Medium |
| **Side-channel resistance** | Vulnerable (timing) | **Resistant** |
| **Patent** | None | None |

**Decision:** ChaCha20-Poly1305 for edge devices (Raspberry Pi, IoT), AES-GCM for cloud (Intel AES-NI)

---

### Zero-Knowledge Proofs (Privacy Layer)

**Use Case:** Prove compliance without revealing data

**Example:**
- Regulator: "Prove this agent didn't exceed debt limit"
- Aurelius: Generates ZK proof: "Agent's debt was ≤ limit"
- Regulator: Verifies proof (yes/no)
- **No transaction details revealed**

**Technology:**
- **zk-SNARKs** (Succinct Non-interactive Arguments of Knowledge)
- Library: circom + snarkjs (JavaScript), or bellman (Rust)
- Circuit: Custom-designed for statutory checks

**Example Circuit (Pseudocode):**

```circom
// Prove: debt < limit, without revealing debt amount

template DebtLimitCheck() {
    signal private input debt;         // Secret
    signal private input limit;        // Secret
    signal input debtHash;             // Public (commitment to debt)
    signal input limitHash;            // Public (commitment to limit)
    signal output valid;               // Public (result)

    // Verify commitments
    debtHash === hash(debt);
    limitHash === hash(limit);

    // Prove debt < limit
    component lessThan = LessThan(64);
    lessThan.in[0] <== debt;
    lessThan.in[1] <== limit;

    valid <== lessThan.out;
}
```

**Result:** Regulator gets 1-bit answer (yes/no), zero information about amounts.

---

## 🏰 Hardware Security Modules (HSMs)

### What is an HSM?

**Hardware Security Module:**
- Physical device (like a USB stick, but hardened)
- Stores cryptographic keys
- Performs signing/encryption INSIDE the device
- **Keys never leave the HSM** (even if server is compromised)

**Tamper Protection:**
- Epoxy-filled casing (drilling triggers self-destruct)
- Temperature sensors (heating/freezing = zeroize keys)
- Voltage sensors (power glitching = zeroize)
- Radiation sensors (X-ray imaging = zeroize)

**Result:** Extracting keys = physically impossible (or so expensive even nation-states struggle)

---

### HSM Providers (Evaluated)

#### Option 1: Thales Luna Network HSM

**Pros:**
- Industry leader (banks, governments use it)
- FIPS 140-3 Level 3 certified
- eIDAS QSCD (Qualified Signature Creation Device) certified
- Supports clustering (high availability)

**Cons:**
- Expensive (~€50k per unit + €10k/year support)
- Proprietary (vendor lock-in)

**Use Case:** Production (we need compliance certifications)

---

#### Option 2: AWS CloudHSM

**Pros:**
- Cloud-native (no hardware to manage)
- Pay-as-you-go (~€1/hour + €0.10/key operation)
- FIPS 140-2 Level 3 certified
- Scales automatically

**Cons:**
- NOT eIDAS QSCD certified (can't be used for legal signatures in EU)
- Shared infrastructure (multi-tenant, albeit isolated)

**Use Case:** Development/testing only

---

#### Option 3: Utimaco SecurityServer

**Pros:**
- European (German, no US export controls)
- FIPS + eIDAS certified
- Better pricing than Thales (~€30k/unit)
- Open APIs (less vendor lock-in)

**Cons:**
- Smaller ecosystem (fewer integrations)

**Use Case:** Viable alternative to Thales (hedge against vendor risk)

---

### Deployment Architecture

```
┌──────────────────────────────────────────────────────┐
│ PRIMARY DATA CENTER (Amsterdam)                      │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  HSM Cluster (N+2 redundancy)              │    │
│  │                                             │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ HSM-A1  │  │ HSM-A2  │  │ HSM-A3  │   │    │
│  │  │ Thales  │  │ Thales  │  │ Thales  │   │    │
│  │  │ Active  │  │ Active  │  │ Standby │   │    │
│  │  └─────────┘  └─────────┘  └─────────┘   │    │
│  │       │             │             │         │    │
│  │       └─────────────┴─────────────┘         │    │
│  │                    │                         │    │
│  │             Load Balancer                    │    │
│  │                    │                         │    │
│  │       ┌────────────┴────────────┐           │    │
│  │       │  Gateway Servers (6x)    │           │    │
│  │       │  (sign requests only)    │           │    │
│  │       └──────────────────────────┘           │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Physical Security:                                  │
│  - Tier IV data center (99.995% uptime)             │
│  - Biometric access (iris + fingerprint)            │
│  - 24/7 armed guards                                 │
│  - Faraday cage (EMI protection)                    │
└──────────────────────────────────────────────────────┘
                          │
                          │ (Encrypted replication)
                          ↓
┌──────────────────────────────────────────────────────┐
│ BACKUP DATA CENTER (Frankfurt)                       │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  HSM Cluster (cold standby)                │    │
│  │                                             │    │
│  │  ┌─────────┐  ┌─────────┐                 │    │
│  │  │ HSM-B1  │  │ HSM-B2  │                 │    │
│  │  │ Utimaco │  │ Utimaco │ (different      │    │
│  │  │ Standby │  │ Standby │  vendor = risk  │    │
│  │  └─────────┘  └─────────┘  mitigation)    │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Activation: Manual (disaster recovery only)         │
│  RTO: 2 hours (Recovery Time Objective)             │
└──────────────────────────────────────────────────────┘
                          │
                          │ (Backup only, no replication)
                          ↓
┌──────────────────────────────────────────────────────┐
│ DISASTER RECOVERY (Offline, Zurich)                 │
│                                                      │
│  - Master key shards (Shamir 3-of-5)                │
│  - Paper wallets (BIP39 seeds)                      │
│  - Encrypted USB drives (AES-256)                   │
│  - Bank vault (UBS, climate controlled)             │
│                                                      │
│  Access: Requires CEO + CTO + 1 board member        │
└──────────────────────────────────────────────────────┘
```

---

### Key Ceremony (Master Key Generation)

**What:** Ritual to generate and secure the master key

**When:** Once (at launch), then every 90 days (rotation)

**Who:**
- CEO (business authority)
- CTO (technical authority)
- CISO (security authority)
- External auditor (witness)
- Notary (legal authority, optional)

**Procedure:**

1. **Preparation (T-1 week)**
   - Schedule ceremony (all parties available)
   - Book secure facility (Tier IV data center)
   - Order new HSMs (factory-sealed)

2. **Day of Ceremony**
   - All parties arrive (no phones, no internet)
   - HSMs unpacked in front of witnesses
   - Video recording (for audit trail)

3. **Key Generation (inside HSM)**
   ```
   HSM> generate_master_key
   Algorithm: EdDSA (Ed25519)
   Output: Master Private Key (never exported)
           Master Public Key (exported, published)
   
   HSM> backup_key_shards
   Scheme: Shamir Secret Sharing (3-of-5)
   Output: 5 encrypted shards
   ```

4. **Shard Distribution**
   - Shard 1 → CEO (sealed envelope → personal safe)
   - Shard 2 → CTO (sealed envelope → home vault)
   - Shard 3 → CISO (sealed envelope → bank vault)
   - Shard 4 → Board member (sealed envelope → lawyer)
   - Shard 5 → Escrow service (sealed envelope → Zurich vault)

5. **Verification**
   - Each party signs receipt (notarized)
   - Auditor verifies all steps followed
   - Video recording archived (encrypted, offline)

6. **Publication**
   - Master public key published:
     - Company website
     - EU eIDAS registry
     - Blockchain (Ethereum, for timestamping)

**Result:** Master key is distributed (no single point of failure), yet recoverable (if 3 parties cooperate).

---

## 🛡️ Threat Model (Detailed)

### Threat 1: Compromised Agent (Malware)

**Scenario:**
- Attacker infects edge device (Raspberry Pi) with malware
- Malware tries to issue unauthorized transactions

**Attack Vector:**
1. Phishing email to agent owner
2. Owner downloads "firmware update" (actually malware)
3. Malware runs on edge device
4. Malware tries to send "SELL ALL ENERGY" command

**Mitigations:**

**Layer 1: Cryptographic Signatures**
- Every command must be signed with agent's private key
- Private key is in HSM (not on Raspberry Pi)
- Malware can't access HSM → Can't forge signatures

**Layer 2: Mandate Validation**
- Even if malware somehow gets a signature, gateway checks mandate
- Mandate: "Max €100/transaction, max 10 tx/day"
- Malware's "SELL ALL" → Rejected (exceeds limits)

**Layer 3: Anomaly Detection**
- AI monitors agent behavior
- "This agent never trades at 3am, now suddenly 100 transactions?"
- Anomaly score > threshold → Agent paused, owner notified

**Layer 4: User Override**
- Owner gets push notification: "Unusual activity detected"
- Owner: "That wasn't me" → Revoke agent keys (instant)

**Result:** Attack fails at Layer 1. Even if Layer 1 bypassed, Layers 2-4 catch it.

---

### Threat 2: Insider Threat (Rogue Employee)

**Scenario:**
- Disgruntled employee with database access
- Tries to steal funds or manipulate transactions

**Attack Vectors:**
1. Direct database manipulation
2. Code injection (malicious commit)
3. Social engineering (trick other employees)

**Mitigations:**

**Layer 1: Principle of Least Privilege**
- No employee has direct database write access (only read, via ORM)
- All writes go through application layer (signed, audited)

**Layer 2: Separation of Duties**
- Developer: Can write code, CAN'T deploy to production
- DevOps: Can deploy, CAN'T write code
- DBA: Can access database, CAN'T access HSM
- Security: Can access HSM, CAN'T access database

**Layer 3: Code Review + CI/CD**
- Every commit reviewed by 2 other engineers
- Automated tests (unit, integration, security)
- Deployment requires approval (2-of-3 senior engineers)

**Layer 4: Audit Logging**
- Every action logged (who, what, when, why)
- Logs are immutable (append-only, cryptographic hashing)
- Logs replicated to external SIEM (Security Information and Event Management)

**Layer 5: Background Checks**
- All employees: Criminal background check
- Employees with HSM access: Additional vetting (references, credit check)

**Result:** Insider has to bypass 5 layers + leave forensic trail. Risk reduced to <0.1%.

---

### Threat 3: DDoS (Distributed Denial of Service)

**Scenario:**
- Attacker floods our servers with fake requests
- Goal: Make system unavailable (no agent can transact)

**Attack Vectors:**
1. Layer 3/4: UDP flood, SYN flood
2. Layer 7: HTTP flood (fake API requests)
3. Amplification: DNS, NTP reflection attacks

**Mitigations:**

**Layer 1: ISP-Level DDoS Protection**
- Provider: Cloudflare Magic Transit or AWS Shield Advanced
- Capability: Scrub >1 Tbps (terabit/sec) attacks
- Cost: €5k-20k/month (worth it)

**Layer 2: Rate Limiting**
- Per IP: 100 requests/minute
- Per agent: 1,000 requests/minute
- Exceeded → HTTP 429 (Too Many Requests)

**Layer 3: Proof-of-Work (PoW)**
- If under attack: Clients must solve puzzle (1 second of work)
- Legitimate clients: Barely notice (1 second delay)
- Bots: Can't keep up (1 second × 1 million requests = too expensive)

**Layer 4: Graceful Degradation**
- If load > 80%: Disable non-critical features (e.g., analytics dashboard)
- If load > 95%: Emergency mode (only critical transactions)
- Core functionality: Always available (even if slow)

**Layer 5: Multi-Region Failover**
- If Amsterdam overwhelmed → Route traffic to Frankfurt
- DNS-based (GeoDNS, latency-based routing)

**Result:** Can withstand 1 Tbps attack (cost attacker €1M+, cost us €10k).

---

### Threat 4: Supply Chain Attack

**Scenario:**
- Attacker compromises upstream dependency (e.g., npm package)
- Malicious code injected into our application

**Examples:**
- event-stream (2018): Bitcoin wallet stealer in npm package
- SolarWinds (2020): Nation-state backdoor in software update

**Mitigations:**

**Layer 1: Dependency Auditing**
- Tool: npm audit, Snyk, or Dependabot
- Run: On every commit (CI/CD pipeline)
- Action: Block deployment if critical vulnerability found

**Layer 2: Dependency Pinning**
- Lock file (package-lock.json, Cargo.lock)
- Never use: `^` or `~` (auto-update = risk)
- Update: Manually, after review

**Layer 3: Subresource Integrity (SRI)**
- For CDN resources (e.g., JavaScript libraries)
- Verify: Cryptographic hash matches
- If mismatch: Refuse to load

**Layer 4: Code Signing**
- All our releases signed with GPG key
- Users can verify: `gpg --verify release.tar.gz.sig`

**Layer 5: Air-Gapped Build**
- Critical components (HSM firmware): Built offline
- No internet access during build (prevent exfiltration)

**Result:** Even if upstream compromised, we detect before deployment.

---

### Threat 5: Quantum Computing (Future)

**Scenario:**
- In 2035, large-scale quantum computer breaks EdDSA
- Attacker decrypts archived transactions, forges signatures

**Timeline:**
- 2026: No threat (quantum computers too weak)
- 2030: Risk emerging (NIST post-quantum standards finalized)
- 2035: High risk (adversarial QC may exist)

**Mitigations:**

**Layer 1: Crypto Agility**
- Our code supports multiple signature algorithms
- Switching from EdDSA to ML-DSA (post-quantum) = configuration change, not rewrite

**Layer 2: Hybrid Schemes**
- Sign with both EdDSA (classical) AND ML-DSA (post-quantum)
- Attacker must break both (hedging strategy)

**Layer 3: Key Rotation**
- Keys expire every 30 days
- Even if attacker breaks old key → Can't forge new signatures

**Layer 4: Monitoring**
- Track quantum computing progress (IBM, Google, etc.)
- Trigger: If 2048-bit RSA broken → Emergency migration to post-quantum

**Layer 5: Data Minimization**
- Don't store data forever (GDPR compliance anyway)
- Old transactions: Archived, then deleted after 7 years
- Less data = less to decrypt

**Result:** We have 5-10 years to migrate (plenty of time, if we start planning now).

---

## 🚨 Incident Response Plan

### Severity Levels

| Level | Definition | Response Time | Example |
|-------|------------|---------------|---------|
| **P0 - Critical** | System down, data breach | 15 minutes | HSM compromised, ransomware |
| **P1 - High** | Degraded service, security risk | 1 hour | DDoS attack, database slow |
| **P2 - Medium** | Non-critical issue | 4 hours | Bug in dashboard, API error |
| **P3 - Low** | Minor issue | 1 business day | Typo in docs, cosmetic UI bug |

---

### P0 - Critical Incident (Example: Ransomware)

**Detection:**
- 02:37 AM: Monitoring alert: "Unusual file encryption activity"
- 02:38 AM: On-call engineer paged (PagerDuty)

**Response (First 15 Minutes):**

**02:40 AM: Assess**
- On-call engineer logs in (VPN + 2FA)
- Confirms: Multiple servers encrypting files
- Conclusion: Ransomware attack

**02:42 AM: Contain**
- Isolate affected servers (firewall rules)
- Disconnect from network (prevent spread)
- Snapshot running processes (forensics later)

**02:45 AM: Escalate**
- Page CISO + CTO (war room)
- Notify CEO (board-level decision needed)
- Contact incident response firm (CrowdStrike or Mandiant)

**02:50 AM: Execute**
- Shut down all non-critical systems (prevent further encryption)
- Verify HSMs not compromised (check tamper logs)
- Restore from backups (last clean snapshot = 01:00 AM)

**03:00 AM: Communicate**
- Internal: Email all employees ("Do NOT log in until further notice")
- External: Status page ("Scheduled maintenance" - don't reveal attack yet)
- Regulatory: Draft notification (GDPR = 72 hours to report breach)

**Response (Next 24 Hours):**

**03:00-06:00 AM: Forensics**
- Incident response firm: Analyze malware sample
- Identify: Attack vector (phishing email? vulnerable software?)
- Determine: Was data exfiltrated? (Check firewall logs)

**06:00 AM: Decision Point**
- If data exfiltrated → GDPR breach notification (inform DPA, users)
- If contained → No breach (business continuity, no notification)

**06:00-12:00 PM: Recovery**
- Restore all systems from backups
- Apply patches (fix vulnerability)
- Change all passwords + rotate keys

**12:00 PM: Resume**
- Bring systems back online (phased rollout)
- Monitor closely (any anomalies?)
- Update status page: "All systems operational"

**Response (Next 7 Days):**

**Day 1-3: Monitoring**
- 24/7 watch (is attacker still in system?)
- Threat hunting (check for backdoors, persistence mechanisms)

**Day 4-7: Post-Mortem**
- Write incident report (timeline, root cause, lessons learned)
- Update runbooks (what worked? what didn't?)
- Improve defenses (e.g., deploy EDR software)

**Response (Next 30 Days):**

**Week 2-4: Communication**
- If breach: Notify all affected users (email + letter)
- Public: Blog post ("What happened, what we learned, what we fixed")
- Regulatory: Submit final report to DPA

**Result:** Attack contained in <1 hour, full recovery in <24 hours, transparency builds trust.

---

## 🔍 Continuous Security

### 1. Penetration Testing

**Frequency:** Quarterly (every 3 months)

**Scope:**
- External: Test from internet (black-box)
- Internal: Test from inside network (gray-box)
- Red Team: Simulate advanced persistent threat (APT)

**Provider:** External firm (e.g., NCC Group, Trail of Bits)

**Deliverable:**
- Report with findings (categorized by severity)
- Proof-of-concept exploits
- Remediation recommendations

**Action:**
- P0/P1 findings: Fix within 7 days
- P2 findings: Fix within 30 days
- P3 findings: Fix when convenient

---

### 2. Bug Bounty Program

**Platform:** HackerOne or Bugcrowd

**Rewards:**

| Severity | Payout | Example |
|----------|--------|---------|
| **Critical** | €10,000 | HSM key extraction, payment bypass |
| **High** | €2,500 | Authentication bypass, SQL injection |
| **Medium** | €500 | XSS, CSRF, rate limit bypass |
| **Low** | €100 | Information disclosure, open redirect |

**Rules:**
- Responsible disclosure (report privately, wait for fix)
- No DDoS, no social engineering
- No attacking production (use staging environment)

**Why do this:**
- Crowd-source security testing (1,000 hackers > 10 employees)
- Build reputation ("We welcome hackers, not fear them")
- Cheaper than breach (€10k bounty << €1M breach cost)

---

### 3. Security Audits (Code + Infrastructure)

**Frequency:** Annually (before each funding round)

**Scope:**
- Code review (all critical modules)
- Architecture review (threat model validation)
- Compliance review (GDPR, AI Act, eIDAS, DORA)

**Provider:** Big 4 (Deloitte, PwC, KPMG, EY) or specialist (Trail of Bits for code)

**Deliverable:**
- Security audit report (for investors, regulators)
- SOC 2 Type II certification (industry standard)

**Cost:** €50k-100k (worth it for credibility)

---

### 4. Employee Training

**Frequency:** Quarterly (mandatory)

**Topics:**
- Phishing awareness (simulate attacks, test employees)
- Secure coding (OWASP Top 10, common mistakes)
- Incident response (everyone knows their role)

**Format:**
- 1-hour online module (KnowBe4 or similar)
- Quarterly phishing simulation (click rate should be <5%)
- Annual in-person training (external expert)

**Metric:**
- Phishing click rate: Baseline 15% → Target <5% (by Year 2)

---

## ✅ Security Roadmap

### Q1 2026 (Foundation)
- [ ] Select HSM vendor (Thales vs. Utimaco)
- [ ] Design key hierarchy
- [ ] Implement basic signing (EdDSA)
- [ ] Set up monitoring (Prometheus + Grafana)

### Q2 2026 (Hardening)
- [ ] Deploy HSM cluster (Amsterdam + Frankfurt)
- [ ] Implement mTLS (all inter-service communication)
- [ ] Set up SIEM (security logs centralized)
- [ ] First penetration test (external firm)

### Q3 2026 (Compliance)
- [ ] eIDAS 2.0 integration (QTSP partnership)
- [ ] GDPR audit (data flows, consent)
- [ ] AI Act documentation (risk management system)
- [ ] SOC 2 Type II preparation

### Q4 2026 (Resilience)
- [ ] Disaster recovery drill (test backup restoration)
- [ ] Incident response tabletop exercise
- [ ] Bug bounty launch (HackerOne)
- [ ] SOC 2 Type II audit (external)

### 2027+ (Continuous Improvement)
- [ ] Quarterly pen tests
- [ ] Annual security audits
- [ ] Post-quantum crypto migration planning
- [ ] ISO 27001 certification (optional, for enterprise customers)

---

**Remember: Security is not a feature, it's a process. We invest continuously, or we fail catastrophically.**

