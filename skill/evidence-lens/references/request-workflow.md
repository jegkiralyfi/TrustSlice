# TrustSlice: REQUEST: turning "not in your view" into an owner decision

**Goal:** when ASK cannot answer from the approved view, the user is not left at a dead end, and nothing is released early.

## When it starts

- ASK returned `NOT_IN_APPROVED_VIEW`, and the user wants the missing information, or
- the user asks directly to request more access to a document's content.

## Rules

1. **Do not confirm existence.** Say only that the information is not in this view. Never reveal whether an excluded value exists, its length, or which file holds it.
2. **Stated, not verified.** The requester's name, role and purpose are recorded as stated by the user. They grant nothing.
3. **No release by request.** A request creates a record only. Access changes only through DEFINE (a new or extended view) and BUILD (owner review), like any other view.

## Steps

1. Ask the user which categories they need and why, in their own words.
2. Prepare a request card: `ticket`, `from_view`, `requested_categories`, `stated_purpose`, `stated_requester`, date, `status: PENDING_OWNER`. Do not copy any source text into it.
3. Show the card and ask for authorization to save it. Delegate `knowledge-agent` `ug-knowledge save-text` to the **requests folder** the administrator named during setup (workflow approval). `waiting_approval` is not saved.
4. On a completed save, tell the user the request is recorded and that the owner decides. If no requests folder is configured, tell the user to contact the document owner instead and save nothing.

## Owner side

- LIST can show pending request cards from the requests folder.
- To grant: the administrator defines an extended view (for example `example-sales-plus-client`) and the owner reviews it in BUILD. To refuse: REVISE the card to `DECLINED`. Either way, the request card is updated, never deleted silently.

See the [worked example](worked-example.md), section 5.
