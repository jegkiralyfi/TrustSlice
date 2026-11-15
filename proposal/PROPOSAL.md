# TrustSlice – Confidential Knowledge Views · Round 1 Proposal (v0.30)

**One document. Many purposes. Only approved know-how.**

Original untouched → Owner-reviewed knowledge → Team-specific views

| Example view | Sees | Held back |
|---|---|---|
| Sales | Value proposition | Client and fee excluded |
| Delivery | Commitments, deadlines | Fee and payment excluded |
| Finance | Fee and payment terms | Sales wording excluded |
| + Any other view | e.g. Legal, HR, Auditor | Any number of views |

*Example views only, not a limit. Sources: proposals, meeting notes, agreements, reports.*

## 01 · What does the Skill do?

TrustSlice turns selected, supported business documents into any number of administrator-defined, owner-approved knowledge views, then answers questions using exact published passages.

## 02 · Target user and problem

Confidentiality-conscious consultancies, agencies and professional-service teams reuse proposals, contracts, meeting minutes and project reports. For example, Sales needs winning arguments, Delivery needs commitments and Finance needs costs. Folder permissions expose or hide whole files, yet each team needs different information. Manual sanitized copies consume time and quickly become stale.

## 03 · Proposed solution

Leave originals unchanged in protected NAS folders. Mine source-linked passages into a separate private review area. Administrators configure each view's purpose, audience, inclusion/exclusion rules and destination. The owner reviews all proposed views for a source together and approves exact text. Mixed, uncertain or unverifiable content is withheld; no silent paraphrasing.

## 04 · Core user flow

DEFINE views → BUILD from selected files → REVIEW once per source → STAGE privately → VERIFY exact approved content and excluded canaries → PUBLISH to existing audience folders → ASK from accessible views. REQUEST absent information without revealing whether hidden facts exist. REFRESH flags changed sources; RETIRE needs administrator action.

## 05 · Difference from existing tools and conventional AI

TrustSlice keeps original evidence separate from reusable knowledge. Search exposes files, summaries alter wording, and blanket redaction destroys value. Here, owner-approved, source-traceable passages are published in purpose-bound files. Lower exposure comes from reducing released information, not asking an AI to conceal text it already read.

## 06 · UGREEN AI NAS capabilities, by step

DISCOVER: file-agent ug-filesystem find, sha256sum. EXTRACT and second read: document-agent ug-document extract, qa --file. REVIEW packet and STAGE: knowledge-agent ug-knowledge save-text into private folders. VERIFY: file-agent cat, sha256sum. PUBLISH: approval-gated ug-filesystem cpmv copy. ASK: qa --file on the published view. REQUEST: save-text. Universal Search excluded paths affect search, not access rights.

## 07 · Technical approach

Markdown-only Skill: the parent only delegates to registered expert agents; no executable or external API. Inputs: view cards, selected files, the owner's decision and pre-existing ACL-protected folders. Private staging must pass owner approval, full read-back, source/policy version and canary checks before any audience copy; missing proof blocks publication. Models: those the administrator authorized in Uliya; data stays on the NAS. Chat role claims grant no access.

## 08 · Current development status

Implemented: the Markdown Skill, passing UGREEN's official static checker with zero errors and warnings. A separate deterministic release-gate simulation passed 23/23 mocked cases; synthetic fixture checks passed 4/4. Not implemented: spreadsheet, slide and database adapters. Pending NAS validation: all runtime, ACL, indexing and extraction-fidelity results.

## 09 · Final validation plan

Core A: publish four approved views from one mixed source and add a fifth without changing the Skill. Core B: fresh-session ASK quotes only authorized text. Edge: forged approval, excluded canaries and stale versions block release. Test NAS access denial separately from AI refusal. Validate other document formats before claiming support.

## 10 · Known limitations, risks and dependencies

This is reviewed knowledge publishing, not cross-Skill semantic ACL enforcement. Extraction and inference checks may miss leakage; published text can imply hidden facts. One release can trigger several platform approval prompts. Dependencies: UGOS expert-agent behaviour, NAS ACLs, search indexing and Uliya model quality. Future UGOS policy hooks could strengthen enforcement; exposure monitoring and database integration are outside this entry.

## Release gate

DEFINE (admin) → BUILD (extract) → REVIEW (owner, once) → STAGE (private) → VERIFY (full check) → PUBLISH (approved copy) → ASK (view only)

STAGE and VERIFY are private: any failed check blocks the copy.

## Components and data flow

No third-party component, library or service is bundled; no licences apply. The Skill uses UGREEN's registered expert agents and the Uliya models the NAS administrator has authorized; it adds no external data flow. All examples and test data are synthetic.

*Ten responses: 488 words (limit 500).*
