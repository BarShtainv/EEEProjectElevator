# SP-06.5 Stage Report

Clean baseline `510250c428ff5cad3155d7beca09d0987a739257` on `main`; Python 3.13.13, pip 26.2, pytest 9.1.1; baseline 425/425 in 1.16s.

`OutputManager` owns one immutable `OutputSnapshot` and exposes the reviewed constructor, `activate`, `next_expiry_ms`, `expire_if_due`, `reset`, and `snapshot`. Initial state is 16 false Boolean channels with null floor/expiry. All 16 floors map to index `floor-1`; activation validates exact floor/time/duration, builds a candidate, and publishes atomically. Durations 100/3000/30000 and large times use exact Python addition. Concurrent/invalid calls raise `StateInvariantError` and preserve state.

Before expiry returns false; at/after expiry clears exactly once; reset atomically clears and cancels old expiry; frozen snapshots remain immutable historical values. No clock/event/controller/watchdog import or behavior exists.

Scoped: 63/63 passed in 0.27s. Full: 488/488 passed in 1.14s. Compile and imports passed. No failures/corrections. Protected paths unchanged; SP-06.6 watchdog remains deferred; no commit/push or deviation.

READY FOR HUMAN REVIEW
