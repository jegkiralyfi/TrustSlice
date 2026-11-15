# TrustSlice: arbitrary-count view registry and owner verification

**Core rule:** views are records, not hard-coded departments. A business administrator can create **any practical number** of named view definitions; processing them is sequential or batched over actual records, never restricted to `Sales`, `Delivery`, `Finance` or any other fixed list. The environment's file-count, disk space, write approval and time constraints still apply.

## View definition card (Markdown data example)

The following card is a *schema illustration*, not a verified NAS configuration or a grant. Actual IDs and paths must come from administrator input, never invented or hard-coded.

| Field | Example / rule |
|---|---|
| `view_id` | `view-projectproposals-01` (stable unique identifier) |
| `view_name` | `Proposal Study - Project Teams` |
| `purpose` | `learn_offer_design` |
| `audience_description` | `approved proposal reviewers` (not authenticated by text) |
| `source_scopes` | explicitly owner-selected source folder references; protected |
| `include_categories` | `VALUE_PROPOSITION`, `DELIVERY_SCOPE` |
| `exclude_categories` | `CLIENT_IDENTITY`, `FEE`, `PAYMENT_TERMS`, `PERSONAL_NOTES` |
| `output_destination` | owner-selected, already-existing NAS folder with appropriate ACL |
| `version` | `1` (increment on change) |
| `state` | `DRAFT`, `OWNER_APPROVED`, `RETIRED`, `STALE` |
| `owner_review` | explicit user-supplied approval record + current source version |
| `expires_on` | optional date; ASK refuses after it (`VIEW_EXPIRED`) |
| `stale_policy` | `warn` (default) or `block` when the source changed after review |
| `approval_mode` | `owner_review_once` only in this competition entry; human review is required before release |
| `review_required_categories` | admin-marked categories (e.g. `CLIENT_IDENTITY`, `FEE`); these are always displayed in the combined review |
| `created_for` | task purpose and intended recipients |

## Example starter cards (examples only: edit before use)

These three cards illustrate one way to split a client contract: Sales, Delivery and Finance are examples, not built-in roles or a limit. Rename, change or delete them, and add any other view (Legal, HR, Auditor, a single project team...).

| `view_id` | include | exclude | `approval_mode` |
|---|---|---|---|
| `example-sales` | `VALUE_PROPOSITION` | `CLIENT_IDENTITY`, `FEE`, `PAYMENT_TERMS` (a separate, owner-approved view can add client and price on request) | `owner_review_once` |
| `example-delivery` | `OBLIGATIONS`, `CLIENT_IDENTITY`, `CONTRACT_DATES`, `DEADLINES` | `FEE`, `PAYMENT_TERMS` | `owner_review_once` |
| `example-finance` | `CLIENT_IDENTITY`, `CONTRACT_DATES`, `DEADLINES`, `FEE`, `PAYMENT_TERMS` | `VALUE_PROPOSITION`, `OBLIGATIONS` | `owner_review_once` |

**Further examples**, not fixed slots: `legal-terms`, `proposal-read`, `accounts-invoice`, `auditor-exception`, `client-project-K`, `external-advisor-summary`. Any other category names and view names are valid if unambiguous and fully configured.

## Persistent structure (example only)

```text
TS_SOURCE/                 # protected originals; never modified by the Skill
TS_PRIVATE_CONFIG/         # view cards, review packets, receipts; owner/admin only
  view-projectproposals-01-v1.md
  review-index-PRJ-042.md
TS_PRIVATE_STAGE/          # approved candidates; fully checked here before any copy
  view-projectproposals-01-v1.md
TS_REQUESTS/               # request cards (ticket, stated need, status)
TS_VIEW_SALES/             # example audience folder; NAS ACL configured by the admin
TS_VIEW_DELIVERY/          # example audience folder
TS_VIEW_FINANCE/           # example audience folder; add one folder per view you define
```

Add `TS_SOURCE/`, `TS_PRIVATE_CONFIG/` and `TS_PRIVATE_STAGE/` to Universal Search excluded paths. This hides them from search results; it is not access control.

A single `manifest.md` can list the view IDs and actual returned paths, but its completeness, creation and maintenance are not guaranteed by a native transactional database. A definition can be listed only if the file-agent finds it and reads it back. Do not silently assume a newly saved file was added to a manifest.

## Publication contract

1. The administrator defines include/exclude categories, business purpose, destination and audience; the original document owner confirms the actual **extracted content** once per source document for all its views, with no unattended auto-publish exception.
2. Mixed or unknown passages stay out until the source owner resolves them.
3. A definition's audience string is not a NAS permission grant; the admin must establish correct read/write ACL and validate by actual user-context test.
4. Never leak raw source paths, true customer names, values or hidden filter predicates into the public view's filename, metadata or quoted citation.
5. Owner-approved text can be reused; the owner must re-review after source hash, policy version, output destination or intended purpose changes.
6. No automatic, silent migration of existing view files if a definition changes: flag stale, rebuild/reapprove and manually restrict old copies.
