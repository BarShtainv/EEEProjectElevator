# SP-02R Narrow Completion Validation

## Scope

Validation is limited to URL repair, prompt tracking, core source traceability, CSV/BibTeX structure, protected PDFs, prohibited product claims, and final Git scope.

## Git and prompt checks

Commands:

```text
git diff --check
git diff --name-only
git status --short
git ls-files 'prompt*.txt'
test -f prompt.txt && test -f prompt2.txt
```

Results:

- `git diff --check`: passed with no output.
- `git diff --name-only`: reported the modified tracked documentation/evidence files; staged prompt index removals and untracked new files are visible in `git status --short`.
- `git status --short`: only SP-02R documentation/evidence changes, two staged prompt index removals, `.gitignore`, the repair audit files, and the two new NIST PDFs are present.
- `git ls-files 'prompt*.txt'`: no output.
- Both local prompt files exist.
- `HEAD` remains `fdad6116376ec9f52adf6abb29f58cbdea128b16`; no commit or push was performed.

## Product URL checks

The exact owner-supplied original URL occurs in:

- `evidence/product_evidence.md`
- `evidence/source_index.md`

The canonical URL remains `https://he.aliexpress.com/item/1005008317933284.html`.

An exact repository search for the known malformed URL encoding returned no match outside ignored local task inputs.

## Claim matrix and source paths

Python standard-library `csv` validation produced:

```text
CSV_HEADER_VALID=yes columns=9
CSV_ROW_WIDTHS_VALID=yes rows=26
ACTIVE_CLAIM_IDS_UNIQUE=yes active=25 superseded=1
CLAIM_ENUMS_VALID=yes
REFERENCED_SOURCE_IDS_EXIST=yes
CLAIM_LOCAL_SOURCE_PATHS_EXIST=yes
```

All four new source IDs are present in `evidence/source_index.md`. The two new local PDF paths exist; the BALTECH and NASA sources are recorded as official webpages with access dates.

## Bibliography

The bibliography check produced:

```text
BIBTEX_KEYS_UNIQUE=yes count=9
BIBTEX_BRACES_BALANCED=yes
```

## Protected and new source hashes

The seven original PDF hashes still equal the SP-02 validation baseline:

```text
388d59a10fb22c683578040be68824025d88ec1fb6973ef40eff84d2f9ece52c  literature/A38x-Functional-Spec-PU0A.pdf
dc4e4aff7c5b00c79c1ff8eed16cf012366506a9cb09a497e20339a711c904d5  literature/ARM® Developer Suite.pdf
bd94feef02b5c7c2853fdfb9523467effaf8ba036d947605c08df302fd5f2a6c  literature/DDI0406C_C_ARMv7_arm_architecture_reference_manual.pdf
b6c82502deb85c8b2940723128dd2577911328c36132c40a6921d6b2939190b7  literature/STM32F101xx_2xx_3xx_5xx_7xx_UM.pdf
22c10369bb4a346758d1f072ec55604d34336e3dc69a2cbed1f8d907be23a778  literature/arm instruction set very good book.pdf
2bdcbdfb03f3c86d5981a74ec44a4044b4b40c71de5a237d2c05d039c59f25ce  literature/arm-instructionset.pdf
495b7c12d3c19f0ff7758585fe05867d04f250f11b541d4178a6f8bfd1a292cb  referenceProject/Example.pdf
```

New official NIST PDFs:

```text
94a4034079bdc47d1b2c71c86e0a652c5976fd7c15ee078d3272c06b4df4a3a0  literature/nist_sp_800_98_rfid.pdf
9ce01f4d67c976edccf0140767399ddc1a0fcbb91cb644c118a6e91e48061f62  literature/nist_sp_800_53_rev5_1.pdf
```

Both new files were recognized as PDF documents. No original PDF or product image changed.

## Scope and claim review

Manual review plus targeted searches confirmed:

- RFID frequency, Wiegand support, processor identity, electrical outputs, and elevator interface remain unknown for the commercial product.
- ARM/STM32 material remains representative external evidence rather than product evidence.
- Wiegand-26 and the 16-bit floor mask remain proposed project choices.
- The abstract 16-floor permission model excludes physical wiring, motors, brakes, doors, passenger-safety control, installation, and certification.
- Elevator integration remains non-blocking for requirements/software modeling and blocking for physical integration claims.
- DEC-008 explicitly requires supervisor or project-owner approval.
- CLM-003 is the active processor-unknown claim and CLM-014 is `superseded`.

## Result

All required narrow checks passed. The literature foundation supports SP-03 without converting the remaining product and physical-integration gaps into verified facts.

READY FOR NEXT STAGE WITH NON-BLOCKING GATES
