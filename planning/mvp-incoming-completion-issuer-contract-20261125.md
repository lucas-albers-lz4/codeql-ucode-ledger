# Same-job incoming queue completion: integration contract (design)

Status: proposed, not implemented or enabled. The offline queue and the event
scan are currently separate branches. A queue MAC authenticates a key holder,
not a scan. No completion may be issued from an uploaded packet, a caller's
JSON assertions, or a standalone offline verifier. Gate 8 remains open.

## Trusted boundary and execution

A reviewed, pinned issuer must run as the final step **inside the same trusted
job** that resolves the event, constructs both source-first oracles, runs the
released producer and invokes the consumer for the head and control. The job
must execute reviewed code from a protected consumer revision, not code from
the untrusted incoming checkout. Incoming source is data only. Pin actions and
verify runner/workflow permissions; prevent the incoming source or processes
it starts from reading the issuer credential or writing trusted executables,
queue database, other job's artifacts, or issuer inputs after verification.
Do not give the HMAC key to PR-controlled code. If this isolation cannot be
established, do not sign. The queue store and signer need a single authorized
owner, durable storage and compare-and-swap predecessor; a MAC does not solve
key custody, runner compromise, replay, or database replacement.

A dispatcher hands the trusted job an authenticated reservation containing
queue ID, event ID, reservation sequence and transition digest, the exact
queued event, and a unique run ID including attempt. The issuer must obtain
these from the queue authority, not an event-supplied artifact. Start is
attested before execution; completion uses the same active run and
reservation. Queue predecessor is re-read immediately before the atomic
transition; stale state is retried only after revalidation, never by creating a
new reservation or replaying another run's result. Recovery revokes the old
reservation and a late completion must fail. Failure, cancellation, timeout,
API drift, or interrupted execution leaves visible pending work, not a
completion. Store failures separately and never label them clean.

## Required verification before emitting

The issuer consumes actual run-owned files through fixed paths, rejects
symlinks/path escapes, duplicate JSON keys, missing/extra schema fields where
specified, and unexpected files or nonzero/absent command statuses. It hashes
bytes itself after writers have stopped, preserves immutable copies, and checks
all links in the following graph. Digest equality alone does not authenticate
execution: these checks are meaningful only under the trusted job boundary.

1. Re-fetch the PR detail in the scan job and run `incoming_event.validate`
   against canonical clean checkouts. Compare queue repository, kind, PR,
   head and queued base with the fresh response and resolved receipt; reject
   closed, changed or unsupported provenance. Verify full commit and tree
   from Git, including base tree where required. Recheck source/control HEAD,
   trees and cleanliness at end. The #160 resolver now records a separately
   fetched canonical base commit and tree; the eventual issuer must verify
   that identity and the post-scan source state. Default
   tips need an equivalent independent resolver and are rejected until then.
2. Require a fully pinned reviewed `r3-release-lock.json`, successful R3
   verification, exact lock bytes and verified release/CLI/pack identities.
   Confirm both event and control use that same lock and the same run ID.
   The current lock has null release fields, so this condition cannot pass.
3. Replay the source-derived event inventory and manifest from the verified
   checkout and pinned policy before scanning. Verify the exact selected and
   excluded identities, source hashes, Git blobs, projected destinations,
   conditions and route oracle, rejecting drift, collisions and duplicates.
   Recompute source and staged hashes after scanning. Check routing multiset,
   successful extraction multiset and diagnostics against that manifest,
   including multiplicity and zero unexpected errors. Bind the actual
   `out/producer-receipt.json` as `extraction_sha256`; it includes successful
   identities, errors, command receipts and route digest. Also retain and
   cross-check `out/coverage-event.json`, routing and raw diagnostic outputs.
4. Hash actual `out/default-suite.sarif`, compare its digest to both producer
   and corpus receipts, and verify the same bytes were passed to the actual
   consumer. Require successful consumer command and parse its actual
   `out/triage.json`, checking its digest against the corpus receipt. Map
   `clean_scan` to `clean` only with zero results; map `triage_required` to
   `alert_triage` only with all results retained for triage. Unknown or
   inconsistent status is a failure. An alert is not an accepted exception.
5. Independently verify control checkout commit/tree and distinctness from the
   event, replay its pre-scan source oracle, and perform the same release,
   manifest, routing, exact extraction, SARIF and consumer checks. Verify
   `control-assertion.json` links the exact binding, control scan receipt and
   triage bytes and asserts zero results; also inspect actual triage and SARIF.
   Bind the assertion bytes as `control_sha256` and retain the full linked
   graph. A zero-result SARIF without successful extraction and consumer
   checks is not a clean control.
6. Verify the run and all commands completed successfully, no failure marker
   exists, provenance identities agree across both scans, and post-run source
   checks passed. Retain phase timings and peak memory if available. Freeze
   and hash the complete artifact inventory, record trusted workflow revision,
   job/run/attempt and issuer revision, then create the exact queue payload.

The queue's current completion shape contains `source`,
`release_lock_sha256`, `manifest_sha256`, `extraction_sha256`, `sarif_sha256`,
`consumer_disposition`, and `control_sha256` alongside reservation fields.
These are hashes of the actual bytes named above, never values accepted from a
caller. Its shape lacks explicit event-receipt, consumer-triage and job
identity digests; extend the schema to bind a canonical issuer receipt that
contains these and the full artifact inventory, before production use. A
single control assertion digest indirectly links other files only if every
link is checked and retained. Queue transition and issuer receipt should each
record their respective schema version. Do not claim the present prototype
already makes these bindings.

## Acceptance controls before enabling an issuer

Use temporary isolated queue databases and fake, source-derived fixture
checkouts. A successful fixture exercises the real resolver, oracle and
consumer interfaces, verifies exact identities and multiplicity, and yields
one completion for its active reservation. It is an offline contract test,
not evidence that a scan happened. Independently mutate one boundary at a time:

- wrong queue ID, event/PR/repository, reservation digest, run ID, predecessor,
  stale recovered reservation, or changed/closed PR; all must reject;
- event or control commit/tree mismatch, dirty checkout, base drift, altered
  policy, source bytes, blob, route, missing/duplicate extraction identity or
  a diagnostic error; all must reject;
- null or altered lock, mismatched release/CLI, failed or missing producer or
  consumer command, mismatched SARIF bytes/digest, unselected URI, malformed
  result or status/count disagreement; all must reject;
- swapped control, nonempty control results, failed control scan, mismatched
  binding/assertion/triage digest, reused event receipt as control, or
  different control run/lock; all must reject;
- artifact substitution after hashing, path escape/symlink, duplicate JSON
  keys, stale packet from a different job or attempt, forged MAC, and valid
  MAC over fabricated evidence: verification must reject each as applicable;
  the final case specifically confirms that MAC validity is insufficient.

Finally run the known positive and independently clean control through the
released Linux event path, with a real queue reservation and issuer, inspect
exact locations and all extracted identities, and test drift/failure recovery.
Review the retention, runner isolation, credential provisioning and queue
ownership before scheduling. A successful offline test or manually assembled
packet is not this drill, and a clean control does not prove security.
