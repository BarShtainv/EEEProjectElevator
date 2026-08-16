# Final Figure Visual-Design Pass

## Baseline and scope

- Date: 2026-08-16
- Branch: `main`
- Starting commit: `43ab8f82e34ea31de11291ea1c17d043e1b186ad`
- Starting status: clean
- Scope: visual styling only for the eight figures already selected for the grading report.

No engineering meaning, topology, state transition, requirement, report conclusion, experiment value, category order, axis value, unit, or accepted SP-07 quantitative artifact was changed. `report/final_report.md` and every accepted data/result file remain unchanged.

## Visual system

The selected Mermaid diagrams now use reusable semantic classes and one restrained engineering palette:

- navy `#274C77`: implemented controller and primary software model;
- teal `#2F7F7B` with pale teal fills: validated data and processing;
- muted green `#4E7D57` with pale green fills: successful logical output and normal service;
- muted amber `#B7791F` with pale amber fills: decisions, priority checks, and active timing;
- muted red `#A44A4A` with pale red fills: denial, logging failure, watchdog expiry, reset, and fault paths;
- blue-gray `#607D8B`: external logical inputs, clocks, and conceptual supporting elements;
- dashed neutral gray `#7A828A`: explicitly excluded physical, safety, and commercial-equivalence scope.

The diagrams use a white background, dark neutral arrows and labels, consistent borders, and shape/label/dash redundancy so color is not the only semantic carrier. Grayscale contact-sheet inspection retained useful luminance and boundary distinctions.

## Architecture figures

The following Mermaid sources and corresponding SVG/PNG renders were visually regenerated:

1. `system_context`
2. `top_level_architecture`
3. `data_flow`
4. `controller_state_machine`
5. `watchdog_sequence`

All five rendered through Mermaid CLI without error. The state-machine font was increased within the same topology to improve normal-page readability. No transition or state label changed.

## Timing figures

`scripts/style_report_figures.py` verifies the exact accepted SVG SHA-256 before producing each report-use PNG. It alters only visual attributes and asserts that every text value, geometry field, data attribute, point, whisker, median, axis position, and non-style attribute remains identical in memory.

Protected accepted SVG hashes remain byte-for-byte unchanged:

- mixed controller: `7ad5f26515f55051794d39a61071c3fc1011e1a28a7ed56f73a71649d2d46930`
- lookup: `26269c6243bae35ada6c7119878ff29799718c79f75052456d8fea84ae2ca096`
- authorization: `433943136faf100dba84a68769d087ffb91b4c4d6914571d4948f0b9257592f9`

The styled PNGs retain the accepted black/gray axis geometry and add a muted blue median series, teal repetition markers, neutral whiskers, gray grid lines, dark labels, and a white background.

## Document rebuild and inspection

- DOCX: `report/final_report_grading_draft.docx`, SHA-256 `1e542882d3a01555cb442ea7b16710e20aeb2ad787e0e78be9fd4f55c3833586`
- PDF: `report/final_report_grading_draft.pdf`, 26 A4 pages, SHA-256 `466e4c7f9cd2d9800234401f52b8a9b0b0e98668fddfe622020ec30f8d6d98f0`

The five architecture figures and three timing figures were inspected at native resolution, in grayscale contact sheets, and at final PDF page scale. Captions remain attached. No clipping, missing figure, low-contrast label, broken Mermaid render, unresolved field, or layout regression was observed. The controller state machine remains necessarily dense because it preserves every reset edge and transition label; it is readable when viewed at normal PDF page scale but is the least compact of the selected figures.

## Validation

Focused report/figure inspections: 96 passed in 1.72 seconds.

`python -m pytest -q`: 1,210 passed in 26.40 seconds.
