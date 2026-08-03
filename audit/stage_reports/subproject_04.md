# SP-04 Stage Report

## Baseline and approval basis

- Repository: `BarShtainv/EEEProjectElevator`
- Branch: `main`
- Starting commit: `94b051cfeebed08db8aec9b590fb99d60c87aee3` (`step3`)
- Starting status: clean
- Baseline: `audit/baselines/subproject_04_baseline.md`

The accepted SP-03 commit and frozen requirements were present without conflicting later work. The project owner approved their defaults for SP-04 conceptual design. Supervisor approval remains pending.

## Conceptual hardware result

Fifteen controller-class blocks cover conceptual power/protection, reader interface, conditioning/isolation, frame acquisition, controller core, program/working/credential memory concepts, timer, watchdog, event storage, service/configuration, 16 output channels, driver/isolation boundary, and elevator access boundary. Electrical and physical blocks are explicitly conceptual-only and contain no voltage, rating, component, connector, relay, wiring, or capacity selection.

## Simulator and firmware result

Eleven runtime elements assign frame/profile, credential, authorization, output, coordination, watchdog, logging, clock, configuration, CLI, and harness responsibilities. Mutable state has one owner. Busy detection occurs before validation, and grant activation is gated by successful grant-event append.

## State, processing, and interfaces

The architecture defines seven states: RESETTING, INITIALIZING, IDLE, VALIDATING, LOOKUP, AUTHORIZING, and OUTPUT_ACTIVE. Normal, denial, invalid, busy, timeout, manual-reset, watchdog-reset, and blocked-initialization transitions are explicit. Fourteen logical/conceptual interfaces cover all required inputs, state outputs, service, time, fault injection, logs, CLI/harness, and physical boundaries.

Idle processing follows the frozen validation/decode/lookup/authorization order. During OUTPUT_ACTIVE, the new request is not inspected; one busy event is attempted while the original activation and expiry remain unchanged.

## Logical memory and register model

`docs/register_model.md` defines nine processor-neutral logical memory regions and 19 unique 32-bit-aligned registers from offset `0x0000` through `0x0048`. It provides control/status, timing, source/frame/floor, decoded fields, mask, output/expiry, watchdog, event, and capability views. State, source, event, result, and reason encodings are unique. Floor 1 maps to bit 0, floor 16 to bit 15, and output bits 31:16 remain zero.

## Reset and watchdog

Startup clears runtime and event state before configuration/repository validation. Manual/watchdog reset clears outputs, expiry, and transients while preserving valid configuration, credentials, prior events, and sequence progression. Watchdog service occurs at committed coordinator checkpoints; injected suppression leaves logical time running. Exactly one expiration request initiates reset.

## Event and failure policy

All event fields are always present, using explicit null for unavailable values. Sequence starts at 1 on the first successful append. Canonical event/result/reason names and logical numerical encodings are fixed.

The 19-mode failure table covers every required input, credential, authorization, busy, configuration, reset/watchdog, logger, and repository failure. Initialization failures remain all-inactive and non-operational. A missing grant event prevents activation; other logging failures do not reverse timeout/reset state changes and are exposed to the harness.

## Requirements coverage and diagrams

The mapping has 84 rows. All 60 required requirements are `designed`; all six optional requirements are `deferred_optional`. All 33 cataloged runtime, governance, and conceptual hardware elements map to at least one requirement. No implementation or verification result is claimed.

Created six proposed-architecture Mermaid sources:

- top-level architecture;
- firmware responsibilities;
- controller state machine;
- data flow;
- reset sequence;
- watchdog sequence.

Rendering was optional and was not performed; no dependency was added.

## Human-review items

Review the conceptual hardware boundary, state enumeration, busy-before-validation order, reset preservation, explicit-null events, enumerations, logical register map, initialization fail-closed policy, event-log failure policy, watchdog checkpoints, and mapping coverage. Supervisor confirmation remains pending but does not block SP-05 within the abstract boundary.

## Validation and deviations

Narrow validation passed for file readability, requirement mapping, element coverage, registers, enumerations, states/transitions, interfaces, failure modes, diagrams, terminology, protected hashes, forbidden paths, and Git scope. Details are in `audit/validation/subproject_04_validation.md`.

No requirements, evidence, source, bibliography, context diagram, project plan, workflow handbook, or prior audit record changed. No code, tests, detailed test plan, experiment data, final APIs, or physical/electrical design was created. There were no scope deviations.

## Exact readiness state

READY FOR HUMAN REVIEW
