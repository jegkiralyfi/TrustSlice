# TrustSlice: plain-language messages and language rule

Status codes are for receipts and tests. People see a plain sentence. Use the user's language for the sentence; keep the status code in brackets so it can be traced.

| Status | Say to the user (adapt the view name and next step) |
|---|---|
| `NOT_IN_APPROVED_VIEW` | That is not in the *Sales* view. If you need it, I can send a request to the document owner. |
| `NO_APPROVED_VIEW` | I could not find an approved view you can open. Ask your administrator which view to use. |
| `VIEW_EXPIRED` | The *Auditor* view expired on *date*. The document owner can renew it. |
| `STALE` | The source changed after this view was reviewed. Answers may be out of date until the owner reviews it again. |
| `NEEDS_REVIEW` | This passage mixes information for different teams, so it is held back until the owner decides. |
| `FIDELITY_MISMATCH` | The extracted text differs from the original wording. Please choose the original, exclude it, or accept your own edit. |
| `LEAK_RISK` | This passage might let a reader work out something the view leaves out. Please check it. |
| `CANARY_LEAK` | A forbidden value was detected before publication. The private staged file was blocked. If a copied audience file exists, it may have been exposed: the NAS administrator must restrict or remove it immediately. |
| `waiting_approval` | Waiting for your approval in UGREEN. Nothing is saved yet. |
| `DEFINED_UNVERIFIED` | The view card was sent for saving, but I could not confirm it on the NAS yet. |

Never put an excluded value, a private path or a source hash in a user message.

## Language rule

- Talk to the user in the language they use.
- **Quoted passages stay in their original language and wording.** Translation would break the word-for-word promise.
- If the user asks for a translation of a quoted passage, give it separately and label it clearly: "Translation, not the approved text." Never save a translation as a view unless the owner reviews it as its own view.
