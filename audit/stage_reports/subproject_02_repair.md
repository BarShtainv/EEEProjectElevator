# SP-02R Narrow Completion Report

## Objective and baseline

Complete only the minimum authoritative literature needed to enter Subproject 3 while preserving valid SP-02 work and all product-evidence limits.

The repair began from a clean `main` working tree at `fdad6116376ec9f52adf6abb29f58cbdea128b16` (`Step 2`). Details are in `audit/baselines/subproject_02_repair_baseline.md`.

## Repairs completed

- Corrected the malformed original AliExpress URL in both evidence records; the canonical URL was unchanged.
- Removed `prompt.txt` and `prompt2.txt` from the Git index while keeping both local files, and added `prompt*.txt` to `.gitignore`.
- Changed the SP-01 readiness line to `READY FOR HUMAN REVIEW`; the missing-image/listing limitation remains.
- Added exactly four core authorities:
  - SRC-RFID-001 — NIST SP 800-98 for RFID components, passive tags, LF/HF, format/frequency separation, and security limitations.
  - SRC-WIEGAND-001 — official BALTECH reader documentation for Wiegand reader-to-system use, D0/D1 pulses, frame variation, and parity.
  - SRC-AUTH-001 — NIST SP 800-53 PE-2/PE-3 for credentials, authorization verification before grant, and access logs.
  - SRC-TEST-001 — NASA Software Engineering Handbook guidance for traceability, unit/integration testing, expected results, repeatability, and evaluation.

## Evidence architecture outcome

The claim matrix now supports a proposed credential-input path, initial Wiegand-26 input boundary, authorization decision, proposed 16-bit floor mask, grant/denial event model, and traceable repeatable verification. CLM-003 remains the canonical processor-unknown claim; duplicate CLM-014 is marked `superseded`.

DEC-008 limits the simulator to an abstract 16-floor permission output. It excludes physical wiring, motors, brakes, doors, passenger-safety functions, installation, and certification. Supervisor or project-owner approval remains required.

## Non-blocking gates retained

- Original product images and listing captures are unavailable.
- Commercial processor, protocol, RFID frequency, Wiegand support, firmware, and electrical outputs remain unknown.
- Detailed LF/HF, smart-card, and exact Wiegand-26 field coverage is deferred until a later claim or implementation needs it.
- Physical elevator integration and detailed elevator standards remain outside software scope; a source is desirable for final-report context.
- Formal fail-safe/fail-secure terminology and university formatting rules remain unresolved.

## Deviations

None. Web research was explicitly authorized, four core sources were sufficient, and research stopped at the minimum threshold. Two official NIST PDFs were stored locally; the BALTECH and NASA sources are official webpages recorded with access dates.

## Validation result

The narrow validation passed. Full commands and outputs are in `audit/validation/subproject_02_repair_validation.md`. No original source PDF or product image changed.

## Readiness

READY FOR NEXT STAGE WITH NON-BLOCKING GATES
