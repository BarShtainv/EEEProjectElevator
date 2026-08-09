# SP-08.2HR History Remediation Required

Offending commit: `ba9756d09cbb7525a29ee5fb93baee9a5f75b9c1`.

A sensitive student identifier entered Git history in that commit. Bounded inspection identified the former raw authoritative human-decision path and current gate records as affected paths. Redacting the current tree does not remove prior history exposure. The repository was observed as public during review. Complete history remediation requires explicit repository-owner authorization; no history rewrite or force-push occurred in this stage. Report drafting must not proceed merely because the current tree is sanitized.
