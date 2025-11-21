# 🛡️ Bug Bounty Program: Living Archive Covenant Integrity & TFK Assurance
### Hosted on HackerOne (Simulated)

### **Program Status**: Open (*Public*)

---

## 🎯 Focus and Goal
The primary objective of this Bug Bounty Program is to validate the **immutability** and **integrity** of the **Living Archive Covenant** for the GPT-OSS-120B model. The program focuses on the **Triple-Signed Trust Framework (TFK)**, which relies on three cryptographic pillars:

1. **Cryptographic Hash**: SHA-256 hash of the covenant manifest.
2. **Dual-Chain Anchors**: Anchoring on Bitcoin Testnet and Ethereum Goerli for redundancy.
3. **GPG Signature**: Verification of the manifest file's `.yaml.asc` signature.

Participants are encouraged to identify **weaknesses** that could undermine or compromise any of these three trust guarantees.

---

## 💻 Categories & Rewards

### **1️⃣ Critical Integrity of the Covenant (TFK Proof)**
| Focus Area                        | Target Weakness                                                                                                 | Reward Level         |
|------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------|
| **Hash Manipulation**              | Discovering a vulnerability in hash generation or verification that allows modification of the covenant while retaining the same SHA-256 hash (collision).  | **Critical**         |
| **Blockchain Anchor Falsification** | Proving the ability to bypass or manipulate Bitcoin (TXID) or Ethereum (Smart Contract) anchors.               | **Critical**         |
| **GPG Signature Forgery**          | Compromising the GPG fingerprint (`3FA5...2D3E`) or creating an unauthorized signature for an altered manifest. | **Critical**         |

---

### **2️⃣ Assurance Infrastructure (Heartbeat Stack)**
| Focus Area                            | Target Weakness                                                                                    | Reward Level         |
|----------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------|
| **S3 Object Lock Circumvention**       | Identifying a method to breach the *immutability* of the Heartbeat Log (`s3://living-archive-audit/heartbeat.log`) despite **COMPLIANCE Mode**. | **High**             |
| **Heartbeat False Negative Alerts**    | Exploiting a flaw in the AWS Step Function that allows integrity violations without SNS alerts.    | **High**             |
| **IPFS Gateway Man-in-the-Middle**     | Successfully faking CID fetching (from `Lambda A`), even with manipulated data.                   | **Medium**           |

---

### **3️⃣ Transparency Portal (Web Frontend)**
| Focus Area                   | Target Weakness                                                           | Reward Level         |
|-------------------------------|---------------------------------------------------------------------------|----------------------|
| **Cross-Site Scripting (XSS)**| Injecting client-side scripts in the Transparency Portal (`index.html`).  | **Medium**           |
| **Manifest Display Manipulation** | Manipulating locally displayed hashes **without affecting source manifest integrity**. | **Low**              |
| **Best Practices Improvement** | Recommendations for improving **frontend security** or **usability** (e.g., CORS policies). | **Low**              |

---

## 💸 Reward Tiers (Example Baselines)

| Severity Level | Reward Range (USD)         | Description                                                                                       |
|----------------|-----------------------------|---------------------------------------------------------------------------------------------------|
| **Critical**   | From $15,000               | Breach **immutability** or **forge trust anchors**.                                              |
| **High**       | From $5,000                | Exploiting failures in heartbeat monitoring or permanently disabling audit logs.                 |
| **Medium**     | From $1,500                | Exploitable **web vulnerabilities (e.g., XSS)** or unauthorized access to non-public audit data. |
| **Low**        | $100–$500                  | **Best-practice improvements** (e.g., header misconfigurations, disclosures).                    |

---

## 🚫 **Exclusions (Out of Scope)**

1. **DDoS attacks** or volume tests.
2. Social engineering attacks targeting employees.
3. Issues with outdated browsers (older than the last two major releases).
4. Missing best practices in GitHub repositories (not directly a security flaw).

---

## 🔐 **Submission Guidelines**
1. Submit all findings via **HackerOne**, ensuring detailed reproduction steps for your report.
2. Include logs, demos, or supporting evidence for stronger evaluation.
3. Do not test vulnerabilities in a way that may disrupt the Live infrastructure.

### **Happy Hunting!**
Your contributions secure the future of **digital trust** with the **TFK Covenant Framework**.
