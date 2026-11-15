# Source formats and compatibility boundaries (TrustSlice v0.30)

Scope is **business-document content**, not a promise of universal file-format parsing. A readable file in UGOS Online Office does not establish complete source extraction or audit-grade fidelity through Uliya experts.

1. **Plain text / Markdown** (proposals, minutes, reports): verify source path and hash; read complete content with `ug-filesystem cat` offsets when available; confirm exact approved substrings, no truncation and mixed-section context.
2. **DOCX / searchable PDF**: attempt `document-agent` `ug-document extract --schema mixed --content-scope full` on **actual selected files**; verify the result envelope and coverage; check quotes against the owner-visible original. Page/paragraph IDs may be absent; do not fabricate them, do not certify byte-exact PDF extraction from repeated model calls.
3. **CSV / TSV**: only as explicitly owner-approved plain-text export with verified row/column interpretation, encoding and complete read-back. Not a validated native spreadsheet adapter. Do not treat exported values as verified formula or dependency knowledge.
4. **XLSX / XLS / XLSM**: unvalidated. Hidden sheets, formulas, external references, formatting, comments and pivots require a tested structured cell adapter. Without it return `SOURCE_FORMAT_UNVERIFIED`; request a separate approved text/CSV export if appropriate.
5. **PPTX / PPT**: unvalidated. Slide order, speaker notes, images and embedded charts require tested per-slide provenance; do not invent extraction. If owner supplies and approves text export, treat it as new source, not a lossless conversion.
6. **Databases / ERP / CRM**: OUT_OF_SCOPE; no database CLI/connector is documented in the current Skill Kit. No credential requests, SQL generation or automatic DB reads.
7. **Missing, unsupported, truncated, incompatible, password-protected or suspicious content**: stop publication for that source with `SOURCE_FORMAT_UNVERIFIED`, `INCOMPLETE_EXTRACTION` or `NEEDS_OWNER_REVIEW`; do not substitute another nearby file.

Scope labels such as `CONTRACT`, `PROPOSAL`, `MEETING_MINUTES`, `REPORT`, `TABLE_EXPORT` may be used for owner-facing organization but do not assert parser capabilities or confer rights. The owner must approve the *exact extracted text and its source context* and the target audience separately. Mixed-source aggregation can expose data through joins; require a separately approved combined view and never assume independent per-document releases are jointly safe.

**NAS status:** all format-specific extraction and ACL tests NOT_RUN. Local synthetic fixture integrity does not validate DOCX/PDF/Excel/PPT/DB Uliya runtime behavior.
