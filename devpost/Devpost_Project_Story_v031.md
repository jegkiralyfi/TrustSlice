## Inspiration

Imagine a training firm, for example. One client proposal contains persuasive wording, internal pricing, staff assignments and a named client. Later meeting notes capture delivery promises and sensitive personnel observations. A quarterly project report mixes valuable lessons with private exceptions. Teams such as Sales, Delivery, HR or Finance (examples only) can all benefit from these records, but not from every detail in them.

NAS folder permissions decide who can open a file. They cannot give Sales one paragraph of a file while holding back the price in the next one: **folder permissions work per file, and TrustSlice works per passage.** Today firms solve this with sanitized copies made by hand, which are slow to make, hard to maintain and easy to get wrong.

TrustSlice grew out of our research on controlled knowledge sharing. Its principle is simple to state: each person should get only what they need and are allowed to know, and the owner of the information decides what that is. An AI NAS with Uliya Skills gave us a place to put this principle into everyday work.

## What it does

TrustSlice is a Markdown-only Uliya Skill for UGREEN AI NAS. It turns one mixed business document into separate, owner-approved views, one file per team.

- An administrator defines any number of views. For example, a Sales view can hold reusable positioning, a Delivery view can hold commitments and deadlines, and a Finance view can hold fees and payment terms. An Auditor view can carry an expiry date, and a view can also serve a single project. These are examples, not a fixed list.
- The document owner reviews all proposed views for one source side by side and approves the exact text, once per source.
- The approved passages are published word for word into a NAS folder that has its own permissions. The original is never edited and never copied to a team.
- A team member asks Uliya a question and gets an answer, with a citation, only from the view they can already open.
- If something is missing, the team member can send a request to the owner. The reply never confirms that a hidden value exists.
- When the source changes, the view is marked stale. When a view passes its expiry date, it stops answering.

The same approach works for proposals, agreements, meeting minutes, consulting reports and other business documents whose text can be extracted and verified.

The usual tools work on whole files. Whole-file search exposes more than a user needs. A normal summary can change legally or operationally important wording. Blanket redaction hides the know-how along with the details. TrustSlice keeps the source unchanged and publishes only owner-approved passages, so text the owner did not approve is not in any team file.

## How we built it

We built TrustSlice as a Skill that contains only Markdown: a SKILL.md file and ten linked reference files. It adds no scripts, binaries or external services. The parent Skill only delegates to UGREEN's registered expert agents and uses actions from the official Skill Kit capability catalog (v2.0.0):

- **Discover:** `file-agent` runs `ug-filesystem find` and `sha256sum` on the selected files.
- **Extract and second read:** `document-agent` runs `ug-document extract` and `qa --file`, so we can compare two readings of the wording.
- **Review packet and staging:** `knowledge-agent` runs `ug-knowledge save-text`, into private folders only.
- **Verify:** `file-agent` runs `cat` and `sha256sum` on the staged file.
- **Publish:** an approval-gated `ug-filesystem cpmv` copy runs with `type=copy` and `overwrite=false`.
- **Ask:** `qa --file` reads the published view only.

The workflow runs in seven main steps:

- **DEFINE:** The administrator writes a view card with the purpose, audience, included and excluded categories, source scope and destination.
- **BUILD:** The Skill fingerprints the selected files, extracts their text, links every passage to its source and flags passages that could point to an excluded fact.
- **REVIEW:** The owner approves the exact text and destinations for all views of one source in one decision.
- **STAGE:** The Skill saves only the approved text in a private staging folder.
- **VERIFY:** The Skill reads the staged file back in full. It checks that the text equals what the owner approved, that every approved passage is present, that the source and the view settings have not changed, and that no forbidden test value (a canary, such as the client name) appears.
- **PUBLISH:** The verified file is copied into the team folder with platform approval, and the Skill reads the copy back.
- **ASK:** Uliya answers only from the published view.

REQUEST, REFRESH and RETIRE handle missing information, changed sources and expired views. Any failed check blocks the copy. If a check fails after the copy, the Skill reports a possible exposure and never calls the file safe. No fallback writes directly into a team folder, and NAS folder permissions remain the access boundary.

To test the design without hardware, we built synthetic data and offline tools. They include a synthetic mixed contract with five canary values, realistic synthetic Hungarian offers, invoices and notes, and two paired test worlds that share the same public offer but hold different secrets. An offline scorer compares results with expected answers, and a release-gate simulator written in standard-library Python checks the release rules. These test tools are not part of the Skill, and all data is invented.

The Skill bundles no third-party component, library or service. It uses UGREEN's registered expert agents and the Uliya models the NAS administrator has authorized. Everything is in our public repository: https://github.com/jegkiralyfi/TrustSlice

## Challenges we ran into

- **We checked too late at first.** Our first design scanned for leaked values only after writing a file that a team could already read. We moved every check into a private staging folder, so nothing reaches a team folder before it passes.
- **Search exclusion is not access control.** UGOS Universal Search excluded paths hide folders from search, but they do not control who can open a file. We kept the two apart in every step and added the staging folder to the excluded paths, because a staged file showing up in search would be a leak.
- **Word-for-word fidelity is harder than it sounds.** Text extraction can change wording. We added a second read and a mismatch status, so the owner chooses the original wording, excludes the passage or accepts an edit knowingly.
- **Text can imply what it hides.** A phrase such as "the largest night-shift freight depot" can identify a client without naming it. The Skill flags such passages for the owner, but we state openly that no check can rule out every inference.
- **Safety costs clicks.** One release can trigger several platform approval prompts. An early draft had an automatic mode; we removed it, because unattended publishing would take control away from the owner.
- **We had no NAS in Round 1.** We could not run the Skill on a UGREEN AI NAS yet, so we separated what we verified from what only the NAS can prove, and we claim no runtime security result.

## Accomplishments that we're proud of

- The Skill passes UGREEN's official static checker with zero errors, warnings and info messages.
- Our offline release-gate simulator passes 23/23 mocked cases. We also checked that the tests can fail: removing any single rule, such as the canary scan or the no-overwrite check, makes at least one case fail.
- The synthetic fixture checks pass 4/4, and a SHA-256 manifest guards the test data.
- Views are records, not hard-coded departments, so a fifth or a tenth view needs no change to the Skill.
- A request for missing information never reveals whether a hidden value exists.
- Every claim in our materials states whether we verified it today or whether it waits for the NAS.

## What we learned

- Access and need-to-know are different questions. Folder permissions answer the first one, and the owner's decision per passage answers the second.
- A check that runs after publishing is a report, not a gate.
- An AI that declines to answer is not the same as a NAS that denies access, so our tests record the two separately.
- A chat claim such as "I am the CFO" must grant nothing. Only real NAS permissions and owner approval count.
- A small, verifiable scope beats a broad promise. We limited Round 1 to documents whose text can be checked, instead of promising spreadsheets and slides that we could not test.

## What's next for TrustSlice – Team Views of Confidential Documents

**First, we will prove the workflow on a real NAS.**

- We will define four views (for example Sales, Delivery, Finance and Auditor), add a fifth without editing the Skill, and measure owner review time, approval prompts and how much useful text survives review.
- We will show exact passages, the staged read-back and proof that forbidden values are absent, and we will record PDF and DOCX extraction results.
- We will test real NAS accounts, a forged "CFO approved" line inside a document and unauthorized questions. We will show whether each refusal came from NAS permissions or only from the AI.
- We will check whether the platform approvals for one release can be batched.

**Our vision goes beyond documents and beyond the office.** None of the following is part of this entry, and each step will need its own tests first.

- **Tables can get views too.** The same owner-approved principle can work on spreadsheets, CSV files and other tables. For example, Sales could get the price list without the margin column, and Finance could get totals without client names. This needs cell, sheet and formula provenance and careful handling of hidden sheets.
- **Slides can be shared slide by slide.** A team could receive the approved slides of a deck, while speaker notes stay private unless the owner approves them.
- **Databases can feed views.** ERP and CRM records could flow into approved views through authenticated, read-only connectors with permission checks at query time.
- **The same principle works at home.** Many NAS units serve families, not only firms. For example, a household could give its tax adviser only the income and deduction passages of its documents, or give a babysitter the emergency contacts and allergies from the household sheet without the alarm code or the bank details.
- **The platform could enforce it.** If UGREEN lets a Skill confirm who the user is and filter search by permission before Uliya reads a file, approved views could become enforced access control across the NAS. Continuous monitoring of information exposure could follow as a separate product.
