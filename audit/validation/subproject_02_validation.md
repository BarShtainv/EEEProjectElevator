# SP-02 Validation

## Checks performed

| Check | Method | Result |
|---|---|---|
| SP-01 prerequisite | Read SP-01 baseline, report, validation, ledger, evidence files, and matrix. | Passed; product-capture absence remains recorded. |
| Source inspection | Targeted title, contents, and relevant chapter/page extraction from local PDFs. | Passed; no broad manual summaries or OCR. |
| Required-file/readability | Existence and UTF-8 checks for SP-02 deliverables. | Recorded after final command run. |
| CSV and source IDs | Python standard-library CSV/schema/unique-ID/source-reference validation. | Recorded after final command run. |
| BibTeX | Structural brace and unique-key validation. | Recorded after final command run. |
| Scope review | Search/manual review of ARM, STM32, Wiegand, RFID, elevator, and safety terms. | Recorded after final command run. |
| Protected material | Hash comparison of PDFs; Git changed-path review. | Recorded after final command run. |

## Expected final Git scope

Only allowed SP-02 paths may appear, in addition to protected pre-existing `prompt2.txt`. No source PDF, product evidence file, product image, snapshot, project plan, workflow handbook, implementation path, or unrelated path may be modified.

## Final command results

The required-file check found all 14 SP-02 deliverables. Python standard-library validation reported:

```text
CSV OK: 20 claims; source IDs OK: 21; UTF-8 Markdown OK: 15 files
BibTeX structural OK: 5 unique keys; braces balanced
```

The CSV header was unchanged; all rows have nine fields; claim IDs are unique; evidence classes, statuses, and confidence labels are valid. Every `SRC-*` reference in the matrix and literature notes exists in `evidence/source_index.md`.

`git diff --check` produced no output. The PDF hashes match the SP-01 baseline hashes:

```text
388d59a10fb22c683578040be68824025d88ec1fb6973ef40eff84d2f9ece52c  literature/A38x-Functional-Spec-PU0A.pdf
dc4e4aff7c5b00c79c1ff8eed16cf012366506a9cb09a497e20339a711c904d5  literature/ARM® Developer Suite.pdf
bd94feef02b5c7c2853fdfb9523467effaf8ba036d947605c08df302fd5f2a6c  literature/DDI0406C_C_ARMv7_arm_architecture_reference_manual.pdf
b6c82502deb85c8b2940723128dd2577911328c36132c40a6921d6b2939190b7  literature/STM32F101xx_2xx_3xx_5xx_7xx_UM.pdf
22c10369bb4a346758d1f072ec55604d34336e3dc69a2cbed1f8d907be23a778  literature/arm instruction set very good book.pdf
2bdcbdfb03f3c86d5981a74ec44a4044b4b40c71de5a237d2c05d039c59f25ce  literature/arm-instructionset.pdf
495b7c12d3c19f0ff7758585fe05867d04f250f11b541d4178a6f8bfd1a292cb  referenceProject/Example.pdf
```

Manual scope review found only qualified uses of ARM, STM32, ARMv7, Cortex-M, Wiegand, 125 kHz, 13.56 MHz, MIFARE, ISO 14443, NFC, relay, elevator, motor, brake, door, safety, certification, and compliance terms. No external manual was used as product proof; Wiegand-26 remains proposed; processor and electrical characteristics remain unknown; and the motion/safety boundary remains explicit.

## Final Git status

Final UTF-8, CSV, and source-ID validation passed. `git diff --name-only` identified only the four allowed modified SP-01 canonical files, and `git diff --check` produced no output. Final `git status --short` was:

```text
 M audit/file_change_ledger.md
 M evidence/assumptions_and_unknowns.md
 M evidence/claim_evidence_matrix.csv
 M evidence/source_index.md
?? audit/baselines/
?? audit/stage_reports/subproject_02.md
?? audit/validation/subproject_02_validation.md
?? docs/
?? evidence/literature_notes.md
?? evidence/unresolved_sources.md
?? prompt2.txt
?? report/
```

`prompt2.txt` is the protected, pre-existing task instruction. Every other listed path is explicitly allowed for SP-02. No forbidden path, source PDF, product image, or product snapshot changed.

## Unresolved validation issues

- No image-hash comparison is possible because no product image exists locally.
- Missing authorities recorded in `evidence/unresolved_sources.md` prevent a ready-for-requirements decision; this is an evidence gap, not a structural-validation failure.
