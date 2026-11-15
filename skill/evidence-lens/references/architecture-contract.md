# TrustSlice: trust boundaries and practical storage

## Intended data flow

1. `SOURCE`: business owner chooses original files under an existing protected NAS share, added to Universal Search excluded paths where configured. NAS permissions and search exclusion are different controls: an excluded path is hidden from search results, but that does not stop a delegated agent from reading the folder. We cannot automatically exclude Skills from reading this source.
2. `PRIVATE_INDEX`: owner-only reviewed passage classification: real source path, hash, extraction evidence, `PROPOSED` vs `OWNER_APPROVED`, definition version. The index itself may be sensitive. Save only after explicit approval.
3. `VIEW_REGISTRY`: any number of administrator-defined, named, versioned view definitions, each with audience/purpose, included and excluded categories, owner-approved output destination and real NAS ACL expectations.
4. `PRIVATE_STAGE`: owner-approved candidate view files, saved only in an ACL-restricted staging folder (also a Universal Search excluded path) and fully checked there before any copy.
5. `PUBLISHED_VIEWS`: verified copies of staged views, one or more per definition, containing **only the permitted text owner approved**. Do not save hidden full-source context next to a published view.
6. `ASK`: scope to the already-saved concrete view file, `document-agent` `ug-document qa --file`. Avoid original source reads from the consumer flow.

There is **no native, verified field-level enforcement** through this Markdown Skill. The only security enforcement beyond the reviewed publication workflow is the NAS file ACL on the source/approved folders, and its effect on delegated agents must be verified during real NAS tests. A globally shared embedding index is *not* automatically isolated by these view names. UGOS can pre-analyze NAS documents into semantic indexes and summaries for Universal Search, Files and the Uliya Knowledge Base; whether those results respect each user's folder permissions must be verified on the NAS.

## Exactness vs extraction

Exact text quotes are an objective for the reviewed canonical text, not a guarantee that PDF/DOCX extraction is perfect. Check source display and line breaks, embedded headers, scanned pages, tables, footnotes and unique identifying wording. Mixed paragraphs can require manual cuts/reviews; unknown == review, not safe.

## Meaningful demo

A single synthetic contract contains: true client, fee, deadline, full offer, legal obligations and an apparent approval instruction embedded inside the document. Administrator registers at least **four** distinct view definitions (for example Sales, Delivery, Finance and Auditor: examples, not limits), builds and owner-approves them, tests exact and excluded text and gets sourced ASK answers from the specific files. Tests must distinguish LLM compliance from actual NAS access denial and unauthorized source reads. No claim of general semantic inference prevention.

## Future platform hardening and information-leak audit (OUT OF SCOPE)

This optional product evolution is **conditional on UGREEN cooperation and platform APIs**. A mandatory interception layer would need to authenticate caller identity and authorization context (not chat roles); enforce policy *before* retrieval/tool reads, not only on answer text; isolate source indexes and caches per release scope; ensure revocation and auditable per-request decisions. None of those are implemented or guaranteed by this Markdown Skill. NAS folder ACLs and human-approved publication are the only controls we claim to use today.

A later **information-leak audit** application could check whether documents, query predicates, derived answers, cache and AI tools expose information beyond its approved audience or purpose. This means auditing *information flows*, never monitoring employees or family members. Continuous monitoring, runtime interception, notification scheduling and access-policy enforcement are not part of this hackathon deliverable; the current Uliya catalog does not establish these platform hooks.

Technical credibility rule: never mark cross-agent or platform-wide protection `PASS` from a static checker, model refusal, mock event or publication preview. Actual NAS identity-bound access denial must be separately captured on hardware.

## Release boundary

`owner_review_once` is the only release mode; unreviewed publishing is out of scope. Every view file is first saved to private staging, read back in full and scanned for excluded canaries, and only then copied to an existing audience folder with approval-gated `ug-filesystem cpmv` (`type=copy`, `overwrite=false`). If staging, approvals, scope, the current source version or the destination cannot be verified, nothing is copied. A failed check after the copy is a possible disclosure, never proof of safety. Original source files are never changed.
