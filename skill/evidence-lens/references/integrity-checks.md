# TrustSlice: evidence-fidelity and private pre-publication checks

This contract is a **best-effort gate plus human source review**, not cryptographic attestation of OCR, an information-flow proof or a global DLP engine. Each check returns counts, status and evidence; no check alone approves publication.

## A. Original-text fidelity before staging

1. On the named original, the `document-agent` first performs `ug-document extract`. An additional **separate call to the same expert** (`ug-document qa --file`) asks for the original wording, word for word, and available section/page evidence. Because it is the same model/expert family, this is an advisory *second read*, not statistically independent verification.
2. Compare proposed words to the source evidence after whitespace/line-break normalization. Report `FIDELITY_OK_TEXT`, `FIDELITY_MISMATCH` or `SOURCE_NOT_VERIFIABLE`; never silently rewrite a word, number or punctuation. For plain text accessible as source, `file-agent cat` and deterministic substring comparison should be used where possible. For PDF/DOCX, a human source inspection is required for a verbatim claim.
3. The owner inspects mixed or doubtful extracts in the one consolidated source review. No unresolved excerpt can be included.

## B. Inference-clue probe in owner-private review

1. Put only owner-controlled candidate view text in the private review packet; it never enters the audience index.
2. For each excluded category, question that private packet with `document-agent qa --file` to see whether an allowed phrase reveals a nickname, city, business size or link. `yes` and `unsure` mark `LEAK_RISK`, `no` is **not** proof. An irreversible leakage risk may require withholding an otherwise accurate passage.
3. Never include hidden query predicates, secret canary values or the sensitive original path in an audience view, ASK text or public receipt.

## C. Full private staging check BEFORE publication

1. After owner content approval, save each candidate view ONLY in the private staging folder using `knowledge-agent save-text` and capture the real returned path; if storage cannot be confined there, `STAGE_UNVERIFIED` and stop.
2. `file-agent cat` reads the whole staged file. Compare the entire returned text to the approved canonical text including footer. If incomplete, missing approved content or mismatched, `PUBLISH_BLOCKED`. For plain text use exact character agreement; PDF-derived quotes are still only as verified by the owner.
3. Scan **negative canaries** (literal values barred by this view) against the complete staged file. Each hit is `CANARY_LEAK` → **no copy to the audience folder**. Confirm **positive passages** exist, to avoid an empty but superficially safe release. Count all hits/misses/unsupported checks. Literal matching is not semantic noninterference.
4. Only after the above pass and current source/policy approval may `file-agent ug-filesystem cpmv` copy the staged file to the intended unique audience destination, with gateway approval and overwrite disabled. Never use a direct audience write as a fallback.
5. After copy, read back and compare with staged text and SHA-256 when possible. A failed post-check is `POSSIBLE_EXPOSURE` and requires immediate NAS administrator attention. A post-check cannot erase a previous disclosure; do not describe a failed file as never published.
6. A result is `PUBLISHED_VERIFIED` only when the copied output matches, the known canaries are absent and no unsettled approval or scope remains. Record actual identities/ACL denials only when they were tested on NAS, not from a model refusal.

## Technical boundaries

- An earlier source hash can become stale between approval and copy; check immediately before copy, but native atomic commit/lock is undocumented.
- Administrator must configure ACL for protected source, review/staging, request and audience folders. Search exclusions (Universal Search > Settings > Excluded path) affect discoverability, **not** access rights.
- Independent `sha256sum` of staged/copied text demonstrates bytes match each other, **not** that the original PDF passage was extracted with perfect fidelity.
- `ug-knowledge collect-evidence` against an audience folder can be used as an optional search-visibility probe, but do not treat it as an access-control check.
