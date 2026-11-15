# TrustSlice: Devpost page text (v0.30)

## Project name
TrustSlice – Confidential Knowledge Views

## Elevator pitch (187 characters, limit 200)
One business document. Many legitimate uses. Only approved knowledge. TrustSlice keeps confidential originals untouched while giving teams owner-reviewed knowledge views on UGREEN AI NAS.

## Cover headline / tagline
Share the know-how. Not the whole document.

## Image gallery (upload in this order)
1. `01_Main.png`: One document, many purposes (example views only)
2. `02_Views.png`: Who sees what (Sales, Delivery, Finance are examples, not a limit)
3. `03_Flow.png`: DEFINE → BUILD → REVIEW → STAGE → VERIFY → PUBLISH → ASK
4. `04_Checks.png`: The release gate: nothing reaches a team folder before it is checked
5. `05_Compare.png`: How TrustSlice differs from folder permissions, search, summaries and redaction
6. `06_Status.png`: What is verified today and what waits for the NAS

---

## About the project

### Inspiration: access is not the same as need-to-know
Imagine a training firm, for example. One client proposal contains persuasive wording, internal pricing, staff assignments and a named client. Later meeting notes capture delivery promises and sensitive personnel observations. A quarterly project report mixes valuable lessons with private exceptions. Teams such as Sales, Delivery, HR or Finance (examples only) can all benefit from these records, but not from every detail in them.

Traditional NAS folder permissions decide who can open a file. They cannot decide which *knowledge* a person may reuse from a mixed file. Making separate sanitized copies by hand is slow, hard to maintain and easy to get wrong. TrustSlice serves organizations that care about purpose-limited internal information flow; it is not a mass-market document summary tool.

### What it does: documents in, permissioned knowledge out
An administrator can define any practical number of views. For example: a Sales view for reusable positioning, a Delivery view for commitments and deadlines, a Finance view for fees and payment terms, an Auditor view with an expiry date, or a view for a single project. These are examples, not a fixed list. The owner decides which original passages may enter each view. The original source is never rewritten by the Skill. Approved content becomes a separate, reusable view file in a NAS folder with its own permissions.

The same approach applies to proposals, agreements, meeting minutes, consulting reports and other business documents. **Format support is limited to what we tested:** the Round 1 workflow targets text-extractable documents. Spreadsheets, slides and databases carry extra risks and are not presented as validated integrations.

### How it works
- **DEFINE:** choose purpose, audience, included and excluded categories, source scope and destination.
- **BUILD:** select the NAS files, fingerprint them, extract and trace supported text.
- **REVIEW:** the owner sees all proposed views for one source side by side and approves exact text and destinations, once per source.
- **STAGE:** save only approved text in a private NAS staging folder.
- **VERIFY:** read the staged file back in full, compare it with the approved text, check source and policy versions, confirm required passages and scan for excluded canaries.
- **PUBLISH:** copy the verified file into the chosen team folder with an approval-gated copy; read it back and report the result.
- **ASK:** answer only from a published view the user can already open under real NAS permissions.
- **REQUEST:** ask the owner to extend a view without confirming that hidden data exists.
- **REFRESH / RETIRE:** flag stale or expired views and leave the removal of old copies to the administrator.

### Why it is different: keep the source, publish only the useful knowledge
Whole-file search exposes more than a user needs. A normal summary can change legally or operationally important wording. Blanket redaction destroys useful context. TrustSlice keeps the source evidence unchanged and builds a separate, purpose-scoped knowledge layer from **owner-approved exact passages**. Unpublished content is absent from released view files. That lowers exposure in this workflow; it does not stop other authorized agents from opening original files.

### The UGREEN advantage, step by step
- **Discover:** `file-agent` with `ug-filesystem find` and `sha256sum`.
- **Extract and second read:** `document-agent` with `ug-document extract` and `qa --file`.
- **Review packet and staging:** `knowledge-agent` with `ug-knowledge save-text`, into private folders only.
- **Verify:** `file-agent` with `cat` and `sha256sum`.
- **Publish:** approval-gated `ug-filesystem cpmv` copy (`type=copy`, `overwrite=false`).
- **Ask:** `qa --file` on the published view only.

NAS folder ACLs remain the access boundary. Universal Search **excluded paths** govern search visibility; they are not access control. The Skill adds no external API or custom runtime.

### Technical quality: a pre-publication gate
An earlier design scanned for leaked canaries only *after* writing a potentially readable team file. The current design uses a private staging folder and a verification barrier before any copy. Missing source evidence, an unreadable or truncated staged file, a changed source hash, an unapproved change, a forbidden canary, a missing approved passage, an existing file with the same name or a pending approval all block the copy. A failed check after the copy is reported as a possible exposure, never as safe. There is no fallback that writes directly into a team folder.

There is a cost in friction: one release can trigger several platform approval prompts (the review packet save, then one staging save and one copy per view). Whether they can be batched is a question for the NAS test day.

### Current evidence
- The Markdown Skill passes UGREEN's official static checker with zero errors, warnings and info messages.
- An offline, deterministic release-gate simulator in our repository passes **23/23** mocked cases. It models the Skill's release rules and was checked by removing individual rules: each removal makes a case fail.
- Synthetic fixture integrity checks pass **4/4**.
- None of this proves Uliya runtime behaviour, protection from inference, or NAS access denial. No real NAS run is claimed.

### File types in scope
- **Primary Round 1 scope:** documents with verifiable text extraction, demonstrated on a synthetic mixed contract.
- **Spreadsheets and CSV:** need cell and sheet provenance, formula and hidden-sheet handling, and a dedicated test matrix before any fidelity promise.
- **Slides:** need slide-level provenance, speaker notes and visual-object handling; not validated in this Skill.
- **Databases, ERP and CRM:** need authenticated read-only connectors and query-time security; a roadmap item, not a file-processing claim.

### Finalist proof plan
1. **Utility:** define four views (for example Sales, Delivery, Finance and Auditor) and add a fifth without editing the Skill; measure owner review time, the number of approval prompts and how much approved text is kept.
2. **Fidelity:** show exact passages, source identifiers, staged read-back and negative canary evidence; record the PDF and DOCX extraction results as they come out.
3. **Access boundary:** test with real NAS accounts, a forged "CFO approved" line inside a document and unauthorized questions. Separate a tool-level ACL denial from an AI-generated refusal.

### Platform roadmap, outside the contest Skill
With future UGREEN support for verified user identity, mandatory pre-retrieval authorization and policy-aware indexing, reviewed publishing could grow into enforced semantic access control. Continuous monitoring of information exposure is a separate possible product and is **not implemented here**.

### Components and data flow
No third-party component, library or service is bundled in the Skill. It uses UGREEN's registered expert agents and the Uliya models the NAS administrator has authorized. All examples and test data are synthetic.

## Built with
markdown · ugos-pro · uliya · ugreen-ai-nas · python (offline tests only, not part of the Skill)

## Try it out
- Round 1 deliverables: English proposal PDF and the Markdown-only Skill ZIP.
- Public repository with the Skill, synthetic fixtures, the offline fixture checker and the release-gate simulator: https://github.com/jegkiralyfi/TrustSlice
- No hosted application and no real NAS security result is claimed.
