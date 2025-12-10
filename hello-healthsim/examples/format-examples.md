# Format Examples

Transform HealthSim data into healthcare standard formats.

---

## FHIR R4 Examples

### Patient Resource

**Prompt:**
```
Generate a FHIR R4 Patient resource for a 55-year-old male with diabetes
```

**Output:**
```json
{
  "resourceType": "Patient",
  "id": "patient-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"]
  },
  "identifier": [
    {
      "system": "http://hospital.example.org/mrn",
      "value": "MRN00000001"
    },
    {
      "system": "http://hl7.org/fhir/sid/us-ssn",
      "value": "999-00-1234"
    }
  ],
  "name": [
    {
      "use": "official",
      "family": "Johnson",
      "given": ["Robert", "Michael"]
    }
  ],
  "gender": "male",
  "birthDate": "1970-03-15",
  "address": [
    {
      "use": "home",
      "line": ["123 Main Street"],
      "city": "Springfield",
      "state": "IL",
      "postalCode": "62701"
    }
  ],
  "telecom": [
    {
      "system": "phone",
      "value": "217-555-0142",
      "use": "home"
    }
  ]
}
```

### FHIR Bundle with Multiple Resources

**Prompt:**
```
Generate a FHIR Bundle for a diabetic patient with conditions and medications
```

**Output:**
```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "patient-001",
        "name": [{ "family": "Garcia", "given": ["Maria"] }],
        "gender": "female",
        "birthDate": "1965-08-22"
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        "id": "condition-001",
        "clinicalStatus": {
          "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active" }]
        },
        "code": {
          "coding": [{ "system": "http://hl7.org/fhir/sid/icd-10-cm", "code": "E11.9", "display": "Type 2 diabetes mellitus without complications" }]
        },
        "subject": { "reference": "Patient/patient-001" },
        "onsetDateTime": "2018-03-15"
      }
    },
    {
      "resource": {
        "resourceType": "MedicationRequest",
        "id": "med-001",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
          "coding": [{ "system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": "860975", "display": "Metformin 1000mg" }]
        },
        "subject": { "reference": "Patient/patient-001" },
        "dosageInstruction": [{ "text": "Take 1 tablet by mouth twice daily" }]
      }
    }
  ]
}
```

---

## HL7v2 Examples

### ADT^A01 Admission Message

**Prompt:**
```
Generate an HL7v2 ADT A01 admission message for a patient with pneumonia
```

**Output:**
```
MSH|^~\&|EPIC|HOSPITAL|DEST|DEST_FAC|20250115143022||ADT^A01^ADT_A01|MSG00001|P|2.5.1|||AL|NE
EVN|A01|20250115143000|||SMITH^JOHN^MD
PID|1||MRN00000001^^^HOSP^MR||THOMPSON^MARGARET^A||19521030|F|||456 OAK AVE^^SPRINGFIELD^IL^62702||2175550142|||||999001234
PV1|1|I|MED3A^312^A^HOSP||||1234567890^ROBERTS^MICHAEL^J^MD|||MED||||ADM|||1234567890^ROBERTS^MICHAEL^J^MD|IP||||||||||||||||||HOSP|||||20250114184500
DG1|1||J18.9^Pneumonia, unspecified organism^I10||20250114|A
DG1|2||J96.01^Acute respiratory failure with hypoxia^I10||20250114|A
DG1|3||I48.91^Atrial fibrillation^I10||20250114|A
```

### ORM Order Message

**Prompt:**
```
Generate an HL7v2 ORM message for a CBC lab order
```

**Output:**
```
MSH|^~\&|EPIC|HOSPITAL|LAB|LAB_FAC|20250115100000||ORM^O01|MSG00002|P|2.5.1
PID|1||MRN00000001^^^HOSP^MR||JOHNSON^ROBERT^M||19700315|M
PV1|1|O|CLINIC||||1234567890^CHEN^SARAH^MD
ORC|NW|ORD001|||||^^^20250115100000^^R||20250115100000|NURSE01^NURSE^AMY
OBR|1|ORD001||58410-2^CBC WITH DIFF^LN|||20250115100000||||||||1234567890^CHEN^SARAH^MD||||||20250115100000|||F
```

### ORU Result Message

**Prompt:**
```
Generate an HL7v2 ORU message with HbA1c result
```

**Output:**
```
MSH|^~\&|LAB|LAB_FAC|EPIC|HOSPITAL|20250115140000||ORU^R01|MSG00003|P|2.5.1
PID|1||MRN00000001^^^HOSP^MR||MARTINEZ^MARIA^L||19680522|F
OBR|1|ORD002||4548-4^HEMOGLOBIN A1C^LN|||20250115080000|||||||||1234567890^CHEN^SARAH^MD
OBX|1|NM|4548-4^HEMOGLOBIN A1C^LN||7.8|%|4.0-5.6|H|||F|||20250115140000
NTE|1||Patient has Type 2 diabetes. A1C slightly above target of 7.0%.
```

---

## X12 Examples

### 837P Professional Claim

**Prompt:**
```
Generate an X12 837P for an office visit
```

**Output:**
```
ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250115*1400*^*00501*000000001*0*P*:~
GS*HC*SENDER_ID*RECEIVER_ID*20250115*1400*1*X*005010X222A1~
ST*837*0001*005010X222A1~
BHT*0019*00*000000001*20250115*1400*CH~
NM1*41*2*SPRINGFIELD MEDICAL*****46*1234567890~
PER*IC*BILLING DEPT*TE*2175550100~
NM1*40*2*BLUE CROSS*****46*BCBS01~
HL*1**20*1~
NM1*85*2*SPRINGFIELD MEDICAL*****XX*1234567890~
N3*100 MAIN STREET~
N4*SPRINGFIELD*IL*62701~
HL*2*1*22*0~
SBR*P*18*GRP00100******CI~
NM1*IL*1*DAVIS*JENNIFER****MI*MEM001234~
N3*456 OAK AVE~
N4*SPRINGFIELD*IL*62702~
DMG*D8*19800322*F~
NM1*PR*2*BLUE CROSS*****PI*BCBS01~
CLM*CLM20250115000001*175***11:B:1*Y*A*Y*Y~
HI*ABK:I10~
LX*1~
SV1*HC:99214*175*UN*1***1~
DTP*472*D8*20250115~
SE*25*0001~
GE*1*1~
IEA*1*000000001~
```

### 835 Remittance

**Prompt:**
```
Generate an X12 835 remittance for a paid claim
```

**Output:**
```
ISA*00*          *00*          *ZZ*PAYER_ID       *ZZ*PROVIDER_ID    *250120*1000*^*00501*000000001*0*P*:~
GS*HP*PAYER_ID*PROVIDER_ID*20250120*1000*1*X*005010X221A1~
ST*835*0001~
BPR*I*98.50*C*ACH*CTX*01*999999999*DA*1234567890*1122334455**01*999999999*DA*9876543210*20250120~
TRN*1*CHK20250120001*1122334455~
DTM*405*20250120~
N1*PR*BLUE CROSS~
N1*PE*SPRINGFIELD MEDICAL*XX*1234567890~
CLP*CLM20250115000001*1*175*128.50*30*12*BCBS001234*11~
NM1*QC*1*DAVIS*JENNIFER****MI*MEM001234~
SVC*HC:99214*175*128.50**1~
DTM*472*20250115~
CAS*CO*45*46.50~
CAS*PR*3*30~
AMT*B6*128.50~
SE*15*0001~
GE*1*1~
IEA*1*000000001~
```

---

## NCPDP D.0 Example

### Pharmacy Claim

**Prompt:**
```
Generate an NCPDP D.0 pharmacy claim transaction
```

**Output:**
```
Transaction Header:
  BIN: 610014
  Version: D0
  Transaction Code: B1
  PCN: RXGROUP
  Transaction Count: 1
  Service Provider ID: 1234567890
  Date of Service: 20250115

Patient Segment:
  Cardholder ID: MEM001234001
  Date of Birth: 19680522
  Gender: F
  First Name: MARIA
  Last Name: SANTOS

Insurance Segment:
  Group ID: CORP001
  Person Code: 01
  Relationship Code: 1

Claim Segment:
  Prescription Number: RX78901234
  Product/Service ID: 00093505601
  Quantity Dispensed: 30
  Days Supply: 30
  Compound Code: 1
  DAW Code: 0
  Date Written: 20250110
  Refills Authorized: 5
  Prescription Origin: 1

Prescriber Segment:
  Prescriber ID: 1234567890
  Prescriber ID Qualifier: 01

Pricing Segment:
  Ingredient Cost Submitted: 8.50
  Dispensing Fee Submitted: 2.00
  Usual and Customary: 15.00
  Gross Amount Due: 10.50

Response:
  Transaction Response Status: A (Approved)
  Authorization Number: AUTH20250115001
  Ingredient Cost Paid: 8.50
  Dispensing Fee Paid: 1.75
  Patient Pay Amount: 10.00
```

---

## CSV Export Example

**Prompt:**
```
Generate 3 professional claims as CSV
```

**Output:**
```csv
claim_id,member_id,service_date,provider_npi,principal_diagnosis,procedure_code,charge_amount,allowed_amount,paid_amount,copay,status
CLM20250115000001,MEM001234,2025-01-15,1234567890,I10,99214,175.00,128.50,98.50,30.00,paid
CLM20250115000002,MEM002345,2025-01-15,1234567890,E11.9,99213,125.00,95.00,70.00,25.00,paid
CLM20250115000003,MEM003456,2025-01-15,1234567890,M54.5,99214,175.00,0.00,0.00,0.00,denied
```

---

## SQL Export Example

**Prompt:**
```
Generate INSERT statements for a patient and their claims
```

**Output:**
```sql
-- Patient
INSERT INTO patients (mrn, member_id, first_name, last_name, birth_date, gender)
VALUES ('MRN00000001', 'MEM001234', 'Jennifer', 'Davis', '1980-03-22', 'F');

-- Diagnoses
INSERT INTO diagnoses (mrn, icd10_code, description, diagnosed_date, status)
VALUES ('MRN00000001', 'I10', 'Essential hypertension', '2020-05-15', 'active');

INSERT INTO diagnoses (mrn, icd10_code, description, diagnosed_date, status)
VALUES ('MRN00000001', 'E78.5', 'Hyperlipidemia', '2020-05-15', 'active');

-- Professional Claim
INSERT INTO claims (claim_id, member_id, claim_type, service_date, provider_npi,
                    principal_diagnosis, total_charges, allowed_amount, paid_amount, status)
VALUES ('CLM20250115000001', 'MEM001234', 'PROFESSIONAL', '2025-01-15', '1234567890',
        'I10', 175.00, 128.50, 98.50, 'paid');

-- Claim Lines
INSERT INTO claim_lines (claim_id, line_number, procedure_code, charge_amount, units)
VALUES ('CLM20250115000001', 1, '99214', 175.00, 1);
```

---

## Tips for Format Requests

1. **Be explicit** - "Generate as FHIR R4 Bundle" is clearer than "Generate as FHIR"

2. **Request validation** - "Generate a valid X12 837P" helps ensure proper structure

3. **Combine formats** - "Generate a patient with HL7v2 ADT message and FHIR equivalent"

4. **Specify version** - "Generate as HL7v2.5.1" when version matters
