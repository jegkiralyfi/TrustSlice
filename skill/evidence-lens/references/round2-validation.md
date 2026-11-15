# TrustSlice: NAS Round 2 deployment, evidence and GO/NO-GO

## Runbook for assigned test day (no assumptions)

**D-01 NAS readiness:** confirm Uliya version, registered `file-agent`, `document-agent`, `knowledge-agent`, their advertised CLI actions, availability of selected folders, and names of authenticated NAS accounts. Record environment without credentials.

**D-02 Paths and ACLs:** create or use existing owner-protected source, registry and staging folders and distinct audience-output folders. NAS admin explicitly configures these permissions outside the Skill. Test actual delegated `cat` from a restricted account: gather real `DENIED` result or mark `ACL_UNVERIFIED`. Add the source, registry and staging folders to Universal Search excluded paths, then search as a restricted user: neither the review index, a staged file nor another role's view may appear in Universal Search or Uliya Knowledge Base results; otherwise mark `INDEX_LEAK`.

**D-03 Definitions:** define 4+ view cards (four demos + fifth new view), approve save, record returned `outputFile`; check read-back. If saving definition fails, report `NO_PERSISTENT_REGISTRY` and treat as Scope-Down.

**D-04 BUILD:** ingest selected synthetic documents, SHA-256, extraction, label source evidence, one combined owner content review per document, save only to private staging, fully read back and scan canaries, then copy with approval to an ACL-protected audience folder; record actual save response and read-back, not hypothetical filenames. Track reviewer minutes and the number of owner and platform approvals per document, in the single reviewed mode. Incomplete extraction → `REVIEW`, never "safe".

**D-04b Integrity and canaries:** run the integrity checks and the canary test from the worked example; record every flag and every canary hit. Any canary hit while in private staging blocks release; any `CANARY_LEAK` after audience copy is a possible exposure and `NO_GO` requiring administrator containment.

**D-05 ASK:** fresh session uses only verified approved view. Answer permitted quotation and abstain on excluded fields. Record all called tools and exact file scopes. Another Skill, administrator account or public search path bypass remains a separate test.

**D-05b REQUEST:** from the Sales view ask for client and price; expect "not in this view", an offered REQUEST, a saved request card in the requests folder after approval, and no hint about whether the value exists.

**D-06 Change/revoke:** edit a synthetic source / alter view rule / mark a definition retired; expect old release approval marked invalid, no silent further reuse. The physical published file may still exist; manual NAS ACL/destination change required.

## Evidence states

`NOT_RUN` → no real NAS trace; `PASS_WORKFLOW` → defined, reviewed, persisted and quoted scope only; `PASS_ACL` → a restricted account's file access rejected by the NAS in tested path; `SCOPE_DOWN` → only owner-reviewed manual publishing, no security guarantee; `INDEX_LEAK` → a view, a staged file or the review index surfaces across roles through search or the knowledge base; `NO_GO` → cannot save/read back or serious unreviewed release. `PASS_WORKFLOW` alone is **not** proof of `PASS_ACL`.

## Demo sketch (3 minutes)

0:00 problem / one contract, many uses; 0:20 owner defines four views + adds a fifth; 0:45 source processing, flags (mixed passage, leak risk), one owner content review and private staging; 1:30 canary check BEFORE an approval-gated copy, followed by verified view files; 2:05 different scoped questions in a new session; 2:25 Sales asks for the client: "not in your view" turns into a request; 2:45 forged in-document approval changes nothing. Only show outcomes confirmed on the NAS. No invented times/paths, no private test labels or actual business data.

## Stop conditions

Stop and report if the expert lacks required action, data cannot be read, tool approval remains pending, role permission cannot be verified, path is missing or unexpected. Never turn a security-affecting `NOT_RUN` or `ERROR` into `PASS`.


## Additional source-format validation (not prerequisite to core demo)

Test text minutes and text proposals as business-document alternatives to the canonical mixed contract; require exact-passages, owner approval and prepublication canary checks. DOCX/PDF extraction requires real NAS coverage and visible source comparison. CSV is conditional text export. XLSX/PPTX and database integrations are OUT_OF_SCOPE until format-aware capabilities and provenance are demonstrated. Any unsupported format must stop with `SOURCE_FORMAT_UNVERIFIED`, never silently claim success.
