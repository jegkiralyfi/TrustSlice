# TrustSlice: view lifecycle: expiry, REFRESH and Files tags

A published view is only as good as its source and its approval. This file says how a view goes out of date and how that becomes visible. Nothing here runs on a schedule: every step starts when a person asks.

## Expiry

- A view card may carry `expires_on` (a date), for example a view made for an external auditor.
- ASK checks it first. On or after that date: no answer, status `VIEW_EXPIRED`, and the plain message from [User messages](user-messages.md). The owner can renew it with REVISE (a new approved version) or let it lapse with RETIRE.
- No `expires_on` means the view does not expire by date; it can still become `STALE`.

## REFRESH (owner or administrator asks: "Which views are out of date?")

1. Read the view cards and build receipts from the protected registry folder (`file-agent` `ug-filesystem cat`).
2. For each source recorded in a receipt, delegate `file-agent` `ug-filesystem sha256sum` on the same path. Missing file → `SOURCE_MISSING`; different hash → `STALE`.
3. Also mark views past `expires_on` as `VIEW_EXPIRED`, and views whose card version is newer than the build receipt as `STALE`.
4. Report one line per view: view ID, status, reason, last review date. REFRESH changes nothing by itself; a stale view needs a new BUILD with owner review. ASK on a `STALE` view answers only with a clear warning that the source has changed since review, or refuses if the card says `stale_policy: block`.

## Files tags (optional, visible in the UGREEN Files app)

At setup the administrator may create three tags in the Files app, for example `TS published` (green), `TS review pending` (yellow) and `TS stale` (red). The Skill **never creates, renames or deletes tags**; it only finds them by name and attaches them.

| Moment | File | Tag |
|---|---|---|
| BUILD saved and verified a view | the view file | `TS published` |
| BUILD stopped waiting for the owner | the source document | `TS review pending` |
| REFRESH found a view `STALE` or `VIEW_EXPIRED` | the view file | `TS stale` |

How: delegate `file-agent` to look up the tag with `ug-filemgr tag-get-by-name`, then attach it with `ug-filemgr tag-add-file` (conditional approval). If a tag does not exist or the attach is not completed, report it and continue; tags are a convenience, never the source of truth. Tag names must stay generic: never put a client, amount or view content in a tag name.
