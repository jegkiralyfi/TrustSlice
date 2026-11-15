# TrustSlice – Team Views of Confidential Documents · Round 1 Proposal (v0.31)

**Each team sees only what it needs.** Share the know-how, not the whole document.

The original stays private → The owner approves parts → Each team gets its own file

| Example view | Sees | Held back |
|---|---|---|
| Sales | Value proposition | Client and fee excluded |
| Delivery | Commitments, deadlines | Fee and payment excluded |
| Finance | Fee and payment terms | Sales wording excluded |
| + Any other view | e.g. Legal, HR, Auditor | Any number of views |

*These views are examples, not a limit. Sources can be proposals, meeting notes, agreements or reports.*

## 01 · What does the Skill do?

The owner decides which parts of a confidential document each team may use. TrustSlice publishes those parts word for word, one file per team, and answers questions only from them.

## 02 · Target user and problem

Consultancies, agencies and professional-service firms reuse proposals, contracts, minutes and reports that hold confidential client details. For example, Sales needs winning arguments, Delivery needs commitments and Finance needs costs. Folder permissions show or hide whole files. Hand-made sanitized copies take time and soon go out of date.

## 03 · Proposed solution

Originals stay unchanged in protected NAS folders. The Skill extracts source-linked passages into a private review area. Administrators define each view's purpose, audience, rules and destination. The owner reviews all views for one source together and approves exact text. Uncertain or mixed passages are held back, never paraphrased.

## 04 · Core user flow

DEFINE views → BUILD from selected files → REVIEW once per source → STAGE privately → VERIFY wording and forbidden values → PUBLISH to team folders → ASK from accessible views. REQUEST never reveals whether a hidden fact exists. REFRESH flags changed sources; RETIRE needs an administrator.

## 05 · Difference from existing tools and conventional AI

TrustSlice keeps the original apart from the passages teams reuse. Search exposes files, summaries alter wording and redaction destroys value. Here, the owner approves source-traceable passages, published in one file per team. Exposure falls because less is released, not because an AI hides text it already read.

## 06 · UGREEN AI NAS capabilities, by step

DISCOVER: file-agent ug-filesystem find, sha256sum. EXTRACT and second read: document-agent ug-document extract, qa --file. REVIEW packet and STAGE: knowledge-agent ug-knowledge save-text into private folders. VERIFY: file-agent cat, sha256sum. PUBLISH: approval-gated ug-filesystem cpmv copy. ASK: qa --file on the published view. REQUEST: save-text. Universal Search excluded paths affect search, not access rights.

## 07 · Technical approach

The Skill is Markdown only; it delegates to expert agents and adds no executable or external API. Inputs are view cards, selected files, the owner's decision and existing ACL-protected folders. A staged file must pass approval, full read-back, version and forbidden-value checks before any copy; missing proof blocks publication. Uliya uses only administrator-authorized models; data stays on the NAS. "I am the CFO" in chat grants no access.

## 08 · Current development status

The Markdown Skill is complete and passes UGREEN's official static checker with zero errors and warnings. An offline release-gate simulation passed 23/23 mocked cases; synthetic fixture checks passed 4/4. Spreadsheet, slide and database adapters are not built. Runtime, ACL, indexing and extraction-fidelity results still need the NAS.

## 09 · Final validation plan

Test 1 publishes four approved views from one mixed source, then adds a fifth without changing the Skill. Test 2 checks that a fresh chat quotes only approved text. Forged approvals, forbidden values and outdated sources must block release. We test NAS access denial separately from AI refusal.

## 10 · Known limitations, risks and dependencies

TrustSlice controls publishing; it does not stop other Uliya Skills from reading originals. Extraction and inference checks may miss leakage, and published text can imply hidden facts. One release can trigger several approval prompts. It depends on UGOS expert agents, NAS ACLs, search indexing and Uliya model quality. Exposure monitoring and database integration are outside this entry.

## Release gate

DEFINE (admin) → BUILD (extract) → REVIEW (owner, once) → STAGE (private) → VERIFY (full check) → PUBLISH (approved copy) → ASK (view only)

In private staging (STAGE and VERIFY), any failed check blocks the copy.

## Components and data flow

No third-party component, library or service is bundled; no licences apply. The Skill uses UGREEN's registered expert agents and the Uliya models the NAS administrator has authorized; it adds no external data flow. All examples and test data are synthetic.

*The ten responses contain 490 words (the limit is 500).*
