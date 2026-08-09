# Final Engineering Report Human Review Request

## Review target and status

This request is addressed to the project owner and supervisor for structured human technical review of **Final Project Controlled Floor Elevator**.

- Draft path: `report/final_report.md`
- Draft starting commit: `e47e8ce537322a4ca20a921a11f2d8dd5c669bbc`
- Draft word count: 6,707
- Structure: exactly fifteen numbered main sections
- Status: complete human-review draft; not an approved final submission
- Technical boundary: deterministic Python software simulation of an abstract access-authorization layer only

No final university submission approval has occurred. The model does not validate a physical reader, electrical output, elevator installation, passenger-safety system, commercial controller, or production deployment. Human review is requested for engineering accuracy, evidence discipline, chapter quality, and report communication. The reviewer is not being asked to rerun the already accepted software verification or independently recompute validated quantitative totals unless the reviewer chooses to do so.

## How to review

Please review the draft against the checklist below. Record required corrections separately from recommendations, and identify material that is explicitly accepted without change. Feedback may refer to a section, subsection, table, figure, paragraph, citation, or precise wording. `None` is acceptable where a response section has no feedback.

The final submission due date is not a prerequisite for reviewing this draft. It remains a separate SP-08.4 administrative input and must not delay technical review.

## A. Overall engineering accuracy

Please evaluate:

- whether the report accurately describes the completed project;
- whether the software-only scope is clear;
- whether any technical statement is misleading;
- whether any important implemented behavior is missing; and
- whether any project-specific design choice is incorrectly presented as commercial-product fact.

## B. Abstract and introduction

Please assess whether:

- the engineering problem is clear;
- the project objective is clear;
- the main correctness and bounded quantitative results are represented accurately;
- the limitations are proportionate;
- the abstract is concise enough; and
- the introduction provides adequate motivation without overclaiming.

## C. Product evidence

Please assess whether:

- the distinction between the motivating commercial item and the proposed reference design is understandable;
- unknown commercial properties remain clearly unknown;
- the absence-of-evidence wording is appropriate; and
- product imagery should remain excluded given unavailable provenance and reproduction permission.

## D. Literature review

Please assess whether:

- RFID background depth is sufficient;
- Wiegand background depth is sufficient;
- authorization and access-control literature is sufficient;
- the representative ARM, STM32, and Marvell discussion is useful or excessive;
- the distinction between representative embedded literature and product evidence is clear; and
- any accepted external source should be removed or emphasized more strongly in the final report.

## E. Requirements and system boundary

Please assess whether:

- the 16-floor model is explained adequately;
- the project-specific `PROJECT_WIEGAND_26` profile is explained adequately;
- floor-mask behavior is understandable;
- busy precedence is understandable;
- simulated output, watchdog, and reset behavior is understandable; and
- physical elevator and passenger-safety exclusions are clear.

## F. Architecture

Please assess whether:

- the architecture decomposition is understandable;
- responsibility and state ownership are clear;
- the logical-register concept is useful;
- any architecture subsection requires expansion or reduction;
- all planned Mermaid diagrams should be included in the formatted report; and
- any planned diagram is unnecessary.

The seven deferred architecture diagram sources are:

- `docs/figures/system_context.mmd`
- `docs/figures/top_level_architecture.mmd`
- `docs/figures/firmware_architecture.mmd`
- `docs/figures/controller_state_machine.mmd`
- `docs/figures/data_flow.mmd`
- `docs/figures/reset_sequence.mmd`
- `docs/figures/watchdog_sequence.mmd`

No diagram has been rendered by this review-packet stage.

## G. Software design

Please assess whether:

- the Python implementation explanation is sufficiently technical;
- too much implementation detail is present;
- too little implementation detail is present;
- the distinction between Python host software and embedded firmware is clear; and
- module responsibilities are understandable without source-code listings.

## H. Verification methodology

Please assess whether:

- the historical 976-test SP-06 verification snapshot is explained clearly;
- requirements-to-test traceability is clear;
- deterministic workload construction is clear;
- the mixed controller and isolated-operation boundaries are understandable; and
- the one-host scope and exactly three measured repetitions are stated clearly enough.

## I. Results

Please confirm the presentation quality—not a mandatory independent recomputation—of:

- 39,000 mixed requests;
- 15,600 grants;
- 19,500 denials;
- 3,900 invalid frames;
- the denial-reason reconciliation;
- 24,000 isolated operations;
- zero lookup mismatches;
- zero incorrect authorization outcomes;
- the timing-summary table; and
- the three accepted SP-07 figures.

## J. Results interpretation

Please assess whether:

- no inappropriate cross-family ranking occurs;
- non-monotonic observations are described fairly;
- the three-repetition limitation is sufficiently visible;
- the lack of raw per-call data is sufficiently visible;
- the report avoids implying statistical significance;
- the report avoids implying constant-time or asymptotic behavior; and
- conclusions from timing are appropriately conservative.

## K. Limitations

Please assess whether the limitations section adequately covers:

- product evidence gaps;
- representative rather than product-specific literature;
- the software-only abstraction;
- physical-integration exclusion;
- safety exclusion;
- one-host scope;
- exactly three repetitions;
- no retained raw per-call samples;
- deterministic constructed workloads;
- distinct operation boundaries;
- no statistical inference; and
- no commercial equivalence.

## L. Conclusions and future work

Please assess whether:

- every conclusion is supported by completed evidence;
- the conclusions are too strong or too weak;
- future work is clearly separated from completed work;
- optional and deferred requirements are described appropriately; and
- hardware or physical future work is correctly framed as separately authorized future work.

## M. References

Please assess whether:

- IEEE citation style is acceptable;
- eight external references are sufficient for the project's current evidence scope;
- any citation appears unnecessary;
- any accepted citation should be used more strongly; and
- incomplete educational sources should remain excluded.

One known, non-blocking provenance-reconciliation item should be handled in the later revision-closure stage: `RPT-027` in `report/report_claim_source_matrix.csv` retains an older `pending_human` status whose blocking input includes citation style. Later authoritative human decisions selected IEEE citation style, and the accepted draft correctly uses IEEE-style numbered citations. This historical row is not being repaired in the packet stage and does not make the IEEE choice unauthorized. Please state whether the RPT-027 provenance note should be reconciled during revision closure.

Do not introduce a minimum reference count unless a reviewer independently supplies an authoritative requirement or decision.

## N. Appendices

Please assess whether:

- the traceability summary is useful;
- the experiment configuration summary is useful;
- the reproducibility commands are useful;
- the accepted artifact inventory is useful;
- the deferred-requirements and evidence-gap summary is useful; and
- any appendix should be moved, removed, or expanded.

## O. Readability and balance

Please assess whether:

- any section is too long;
- any section is too short;
- unnecessary repetition remains;
- technical terms require additional explanation;
- tables improve readability; and
- the overall chapter balance is suitable for a B.Sc. final engineering project.

## P. Final document preparation

Please provide preferences for:

- which architecture diagrams to render;
- figure and table placement;
- caption wording;
- cover-page presentation;
- heading numbering;
- page breaks;
- appendix placement; and
- DOCX styling.

These are preparation preferences, not authorization to create DOCX, PDF, PPTX, diagram renders, or submission artifacts in this stage.

## Required authoritative response path

After completing the review, save the genuine human-supplied response exactly at:

`report/authoritative_inputs/final_report_human_review.md`

This packet does not create that file. Absence of the response is not approval, and an empty revision list is not approval unless the explicit overall review decision provides approval under the semantics below.

## Allowed overall review decisions

Use exactly one of these values for `Overall review decision:`.

- `approved_for_revision_closure` — The draft is technically accepted as the basis for final document production, subject only to explicitly listed bounded revisions and later formatting/submission work.
- `approved_with_required_revisions` — The draft is generally accepted, but the specifically listed revisions must be completed and re-reviewed before document production.
- `major_revision_required` — Substantial report changes are required before final document production.
- `not_approved` — The draft is not accepted as a final-report basis.

No response, an ambiguous response, or feedback without one of these values must not be treated as approval.

## Exact human-response format

Copy the following structure into `report/authoritative_inputs/final_report_human_review.md` and replace bracketed instructions with genuine human decisions. Use `None` in any feedback section where there is no feedback.

```markdown
# Final Engineering Report Human Review

Draft commit:

Reviewer 1 name:

Reviewer 1 role:

Reviewer 2 name:

Reviewer 2 role:

Review date or version:

Overall review decision:

Use exactly one: approved_for_revision_closure | approved_with_required_revisions | major_revision_required | not_approved

## Required revisions

[Human-supplied required changes, or None]

## Recommended revisions

[Human-supplied recommendations, or None]

## Technical corrections

[Human-supplied technical corrections, or None]

## Literature and citation feedback

[Human-supplied literature/citation feedback, including the RPT-027 reconciliation decision, or None]

## Architecture and figure decisions

[Human-supplied diagram and figure decisions, or None]

## Results and discussion feedback

[Human-supplied results/discussion feedback, or None]

## Limitations feedback

[Human-supplied limitations feedback, or None]

## Conclusions feedback

[Human-supplied conclusions feedback, or None]

## Formatting and DOCX guidance

[Human-supplied formatting guidance, or None]

## Items explicitly approved without change

[Human-supplied approved items, or None]

## Reviewer confirmation

We confirm that the contents of this file are genuine human-supplied review decisions for the identified final engineering report draft. We understand that this review does not itself create, release, or submit the final DOCX/PDF or presentation.
```

## Privacy and repository-handling warning

Do not place student identification numbers, signatures, phone numbers, private email addresses, credentials, private portal information, or other private contact details in the repository review file. Ordinary reviewer names and roles may be recorded when the reviewers authorize their use. If sensitive identity or submission information is later required, handle it through an approved private process outside this repository.

The next implementation stage is `SP-08.3R — Human-Review-Driven Report Revision and Closure`. It must not begin until the authoritative response file exists and contains genuine human review.
