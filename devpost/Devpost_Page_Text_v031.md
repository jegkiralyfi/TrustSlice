# TrustSlice: Devpost page text (v0.31)

## Project name
TrustSlice – Team Views of Confidential Documents

## Elevator pitch (182 characters, limit 200)
Each team gets only what it needs and is allowed to know. The owner approves the parts word for word, and TrustSlice never shares the confidential original. It runs on UGREEN AI NAS.

## Cover headline / tagline
Share the know-how, not the whole document.

## Image gallery (upload in this order; the text after each file name can serve as its caption)
1. `01_Main.png`: Each team gets only what it needs and is allowed to know. The views shown are examples.
2. `02_Views.png`: The table shows who sees which part of one contract. Sales, Delivery and Finance are examples, not a limit.
3. `03_Flow.png`: Seven steps take a document from DEFINE to ASK, and the original is never edited.
4. `04_Checks.png`: Nothing reaches a team folder before it is checked.
5. `05_Compare.png`: The usual tools work on whole files; TrustSlice works per passage.
6. `06_Status.png`: The image shows what we verified today and what the NAS tests will check next.

---

## About the project

### Inspiration: access is not the same as need-to-know
Imagine a training firm, for example. One client proposal contains persuasive wording, internal pricing, staff assignments and a named client. Later meeting notes capture delivery promises and sensitive personnel observations. A quarterly project report mixes valuable lessons with private exceptions. Teams such as Sales, Delivery, HR or Finance (examples only) can all benefit from these records, but not from every detail in them.

NAS folder permissions decide who can open a file. They cannot give Sales one paragraph of a file while holding back the price in the next one: **folder permissions work per file, and TrustSlice works per passage.** Making separate sanitized copies by hand is slow, hard to maintain and easy to get wrong. TrustSlice is built for firms that handle client-confidential documents; it is not a general summary tool.

### What it does: one document goes in, and each team gets its own approved file
An administrator can define any number of views. For example, a Sales view can hold reusable positioning, a Delivery view can hold commitments and deadlines, and a Finance view can hold fees and payment terms. An Auditor view can carry an expiry date, and a view can also serve a single project. These are examples, not a fixed list. The owner decides which original passages may enter each view. The Skill never rewrites the original source. Approved text becomes a separate view file in a NAS folder with its own permissions.

The same approach works for proposals, agreements, meeting minutes, consulting reports and other business documents. **We claim support only for formats we have checked:** the Round 1 workflow targets documents whose text can be extracted and verified. Spreadsheets, slides and databases carry extra risks, and we do not present them as validated integrations.

### How it works
- **DEFINE:** The administrator sets the view's purpose, audience, included and excluded categories, source scope and destination.
- **BUILD:** The Skill fingerprints the selected NAS files, extracts their text and links every passage to its source.
- **REVIEW:** The owner sees all proposed views for one source side by side and approves the exact text and destinations, once per source.
- **STAGE:** The Skill saves only the approved text in a private NAS staging folder.
- **VERIFY:** The Skill reads the staged file back in full and compares it with the approved text. It checks that the source and the view settings have not changed, that every approved passage is present and that no forbidden test value (a canary, such as the client name) appears.
- **PUBLISH:** An approval-gated copy places the verified file in the chosen team folder. The Skill reads the copy back and reports the result.
- **ASK:** Uliya answers only from a published view that the user can already open under real NAS permissions.
- **REQUEST:** A team member can ask the owner to extend a view. The reply never confirms that hidden data exists.
- **REFRESH / RETIRE:** The Skill flags stale or expired views, and the administrator removes old copies.

### Why it is different: the source stays, and only useful passages are published
Whole-file search exposes more than a user needs. A normal summary can change legally or operationally important wording. Blanket redaction destroys useful context. TrustSlice keeps the source unchanged and publishes **owner-approved passages, word for word,** in a separate file per team. Text the owner did not approve is not in any team file. This lowers exposure in this workflow, but it does not stop other authorized agents from opening the original files.

### Which UGREEN capabilities each step uses
- **Discover:** `file-agent` runs `ug-filesystem find` and `sha256sum`.
- **Extract and second read:** `document-agent` runs `ug-document extract` and `qa --file`.
- **Review packet and staging:** `knowledge-agent` runs `ug-knowledge save-text`, into private folders only.
- **Verify:** `file-agent` runs `cat` and `sha256sum`.
- **Publish:** an approval-gated `ug-filesystem cpmv` copy runs with `type=copy` and `overwrite=false`.
- **Ask:** `qa --file` reads the published view only.

NAS folder ACLs remain the access boundary. Universal Search **excluded paths** control what search shows; they are not access control. The Skill adds no external API or custom runtime.

### Technical quality: a gate before publication
Each team file is first saved and checked in a private staging folder. The copy is blocked if source evidence is missing, the staged file is unreadable or truncated, the source hash has changed, the text differs from what the owner approved, a forbidden canary appears, an approved passage is missing, a file with the same name already exists or an approval is still pending. If a check fails after the copy, the Skill reports a possible exposure and never calls the file safe. No fallback writes directly into a team folder.

This safety costs some friction: one release can trigger several platform approval prompts (the review packet save, then one staging save and one copy per view). On the NAS test day we will check whether they can be batched.

### Current evidence
- The Markdown Skill passes UGREEN's official static checker with zero errors, warnings and info messages.
- An offline, deterministic release-gate simulator in our repository passes **23/23** mocked cases. It models the Skill's release rules. We checked it by removing individual rules, and each removal makes a case fail.
- Synthetic fixture integrity checks pass **4/4**.
- None of this proves how Uliya behaves at runtime, that a reader cannot work out a hidden fact from approved text, or that the NAS denies access. We claim no real NAS run.

### File types in scope
- **The primary Round 1 scope** is documents whose text extraction can be verified. A synthetic mixed contract demonstrates it.
- **Spreadsheets and CSV files** need cell and sheet provenance, handling of formulas and hidden sheets, and a dedicated test matrix before we promise word-for-word accuracy.
- **Slides** need slide-level provenance and handling of speaker notes and visual objects. This Skill does not validate them.
- **Databases, ERP and CRM systems** need authenticated read-only connectors and permission checks at query time. They are a roadmap item, not a file-processing claim.

### Finalist proof plan
1. **Utility:** We define four views (for example Sales, Delivery, Finance and Auditor) and add a fifth without editing the Skill. We measure owner review time, the number of approval prompts and how much useful text survives review.
2. **Fidelity:** We show exact passages, source identifiers, the staged read-back and proof that forbidden values are absent. We record the PDF and DOCX extraction results as they come out.
3. **Access boundary:** We test with real NAS accounts, a forged "CFO approved" line inside a document and unauthorized questions. We show whether each refusal came from NAS permissions or only from the AI.

### Platform roadmap, outside the contest Skill
If UGREEN later lets a Skill confirm who the user is and filter search by permission before Uliya reads a file, the same approved files could become enforced access control. Continuous monitoring of information exposure would be a separate product; it is **not implemented here**.

### Components and data flow
The Skill bundles no third-party component, library or service. It uses UGREEN's registered expert agents and the Uliya models the NAS administrator has authorized. All examples and test data are synthetic.

## Built with
markdown · ugos-pro · uliya · ugreen-ai-nas · python (offline tests only, not part of the Skill)

## Try it out
- The Round 1 deliverables are the English proposal PDF and the Markdown-only Skill ZIP.
- The public repository holds the Skill, synthetic fixtures, the offline fixture checker and the release-gate simulator: https://github.com/jegkiralyfi/TrustSlice
- We host no application and claim no real NAS security result.
