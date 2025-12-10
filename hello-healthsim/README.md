# Hello HealthSim!

**Get up and running with synthetic healthcare data generation in 5 minutes.**

HealthSim is a skill-based framework that enables Claude to generate realistic synthetic healthcare data through natural conversation. No coding required - just describe what you need.

## What You'll Build

By the end of this guide, you'll be able to generate:

- **Clinical Data** - Patients with realistic diagnoses, medications, and lab results
- **Claims Data** - Professional and facility claims with proper adjudication
- **Pharmacy Data** - Prescriptions, pharmacy claims, and drug utilization alerts

All through simple natural language requests like:
> "Generate a 65-year-old diabetic patient with hypertension and their recent office visit claim"

---

## Prerequisites

Before starting, ensure you have:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Git | 2.0+ | `git --version` |
| Claude Desktop **or** Claude Code | Latest | See installation links below |
| Anthropic API Key (for Claude Code) | - | [Get API Key](https://console.anthropic.com/) |

### Install Claude (Choose One)

**Option A: Claude Desktop** (Recommended for beginners)
- Download from [claude.ai/download](https://claude.ai/download)
- Requires Claude Pro subscription for extended usage

**Option B: Claude Code** (For developers)
```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or via Homebrew (macOS)
brew install claude-code
```

---

## Quick Start

### Step 1: Clone the Repository

```bash
# Clone HealthSim skills
git clone https://github.com/YOUR_ORG/healthsim-skills.git

# Navigate to the project
cd healthsim-skills
```

### Step 2: Configure Claude

Choose your Claude environment and follow the appropriate guide:

| Environment | Guide | Best For |
|-------------|-------|----------|
| Claude Desktop | [CLAUDE-DESKTOP.md](CLAUDE-DESKTOP.md) | Interactive exploration, non-developers |
| Claude Code | [CLAUDE-CODE.md](CLAUDE-CODE.md) | Developers, automation, CI/CD |

### Step 3: Verify Installation

Once configured, test with this simple prompt:

```
Generate a patient with Type 2 diabetes
```

You should see output like:
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Maria", "family_name": "Garcia" },
    "birth_date": "1962-05-14",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "E11.9", "description": "Type 2 diabetes mellitus without complications" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" }
  ]
}
```

**Congratulations!** You're ready to generate healthcare data!

---

## Your First 5 Minutes

Try these examples to explore HealthSim's capabilities:

### Example 1: Generate a Patient (PatientSim)

```
Generate a 72-year-old male with heart failure and COPD, including recent labs
```

### Example 2: Generate a Claim (MemberSim)

```
Generate a paid professional claim for a cardiology office visit
```

### Example 3: Generate a Pharmacy Claim (RxMemberSim)

```
Generate a pharmacy claim for lisinopril with a drug interaction alert
```

### Example 4: Cross-Domain Generation

```
Generate a diabetic patient with their recent office visit claim and pharmacy claims for their medications
```

### Example 5: Format Transformation

```
Generate an HL7 ADT^A01 admission message for a patient with pneumonia
```

See [examples/](examples/) for more detailed examples with expected outputs.

---

## What's Included

```
healthsim-skills/
├── SKILL.md                    # Master skill file (start here)
├── scenarios/
│   ├── patientsim/            # Clinical/EMR data generation
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   └── ...
│   ├── membersim/             # Claims/payer data generation
│   │   ├── professional-claims.md
│   │   ├── facility-claims.md
│   │   └── ...
│   └── rxmembersim/           # Pharmacy/PBM data generation
│       ├── retail-pharmacy.md
│       ├── dur-alerts.md
│       └── ...
├── formats/                    # Output format transformations
│   ├── fhir-r4.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   └── ...
├── references/                 # Code systems and rules
│   ├── data-models.md
│   ├── code-systems.md
│   └── ...
└── hello-healthsim/           # You are here!
```

---

## Next Steps

Once you're comfortable with basic generation:

### Learn More
- [SKILL.md](../SKILL.md) - Complete feature reference
- [examples/](examples/) - Detailed examples with outputs
- [docs/integration-guide.md](../docs/integration-guide.md) - Cross-skill data flows

### Extend HealthSim
- [EXTENDING.md](EXTENDING.md) - Add new scenarios, formats, and code systems

### Get Help
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Issues](https://github.com/YOUR_ORG/healthsim-skills/issues) - Report bugs or request features

---

## Quick Reference Card

### PatientSim (Clinical Data)

| Request | What You Get |
|---------|--------------|
| "diabetic patient" | Patient + diabetes diagnoses + meds + labs |
| "heart failure patient" | Patient + CHF + GDMT medications + BNP |
| "admission for pneumonia" | ADT event + encounter + orders |

### MemberSim (Claims Data)

| Request | What You Get |
|---------|--------------|
| "office visit claim" | 837P professional claim + adjudication |
| "inpatient claim" | 837I facility claim + DRG + payment |
| "denied claim" | Claim + denial reason + appeal info |

### RxMemberSim (Pharmacy Data)

| Request | What You Get |
|---------|--------------|
| "pharmacy claim for metformin" | NCPDP claim + pricing + copay |
| "drug interaction alert" | Claim + DUR response + clinical info |
| "specialty drug claim" | High-cost drug + prior auth + copay assistance |

### Format Requests

| Add This | Output Format |
|----------|---------------|
| "as FHIR" | FHIR R4 Bundle |
| "as HL7" | HL7v2 message |
| "as 837" | X12 837 EDI |
| "as CSV" | CSV file format |

---

## Success! What Now?

You've just unlocked the ability to generate realistic healthcare test data through conversation. Here are some ideas:

1. **Test Your APIs** - Generate FHIR resources to test your healthcare APIs
2. **Train ML Models** - Create diverse patient populations for training data
3. **Demo Your Product** - Generate realistic scenarios for product demos
4. **Load Test Systems** - Generate bulk data for performance testing
5. **Validate Workflows** - Test claims adjudication and pharmacy workflows

**Happy generating!**

---

*HealthSim is designed for generating synthetic test data only. Never use for actual patient care or real PHI.*
