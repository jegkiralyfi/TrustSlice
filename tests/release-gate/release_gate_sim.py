#!/usr/bin/env python3
"""TrustSlice release-gate simulator (offline, deterministic).

What this is: an executable model of the BUILD release rules written in
skill/evidence-lens/SKILL.md (steps 6-10) and references/integrity-checks.md,
section C. Each case feeds the gate a mocked set of expert-agent returns and
checks the final status and where files were written.

What this is NOT: a test of UGREEN Uliya, the expert agents, NAS ACLs or
extraction fidelity. Every NAS behaviour here is mocked. It is not part of the
Skill package and must not be uploaded to the NAS.

Usage:  python3 release_gate_sim.py [--out result.json]
Python 3 standard library only. Exit code 1 if any case fails.
"""
import argparse
import hashlib
import json
import sys

STAGING = "/TS_PRIVATE_STAGE/"
SOURCE_DIR = "/TS_SOURCE/"
SUPPORTED_FORMATS = {"md", "txt", "docx", "pdf"}

CANONICAL = (
    "Every new hire is paired with a coach in week one, so teams reach full "
    "productivity sooner.\n"
    "View example-sales · v1 · owner_review_once · reviewed 2026-11-15 · source SYNTH-CONTRACT-01\n"
)
CANARIES = ["Quillmoor", "EUR 12,417", "21 days", "Debrecen"]
REQUIRED = ["Every new hire is paired with a coach in week one"]


def sha(text):
    return hashlib.sha256(text.encode("utf8")).hexdigest()


def base_case():
    """A fully valid world. Each test case changes one thing."""
    return {
        "card": {"view_id": "example-sales", "status": "OWNER_APPROVED", "version": 1,
                 "expired": False, "destination": "/TS_VIEW_SALES/"},
        "source": {"path": SOURCE_DIR + "SYNTH-CONTRACT-01.md", "format": "md",
                   "hash_at_approval": "H1", "hash_now": "H1", "hash_before_copy": "H1"},
        "approval": {"kind": "owner_decision", "status": "completed", "source_hash": "H1",
                     "policy_version": 1, "unresolved_flags": []},
        "canonical": CANONICAL,
        "stage_save": {"status": "completed", "outputFile": STAGING + "example-sales-v1.md",
                       "written_text": CANONICAL},
        "stage_readback": {"complete": True},
        "destination": {"exists": True, "conflicting_file": False},
        "copy": {"approval": "completed", "result": "completed"},
        "post_copy_text": None,  # None means: identical to the staged file
    }


def gate(c):
    """Return (status, reason, writes). writes lists (folder_kind, path)."""
    writes = []
    card, src, appr = c["card"], c["source"], c["approval"]

    # Step 1: valid, current view definition with a legal destination
    if card is None or card["status"] != "OWNER_APPROVED" or card["expired"]:
        return "NO_VALID_VIEW_DEFINITION", "card missing, unapproved, retired or expired", writes
    if card["destination"].startswith((STAGING, SOURCE_DIR)):
        return "NO_VALID_VIEW_DEFINITION", "destination inside staging or source", writes

    # Steps 2-3: verified, supported source
    if src["format"] not in SUPPORTED_FORMATS:
        return "SOURCE_FORMAT_UNVERIFIED", "format not validated: " + src["format"], writes

    # Step 6: one explicit owner decision bound to this source and policy version
    if appr is None or appr["kind"] != "owner_decision" or appr["status"] != "completed":
        return "NEEDS_OWNER_REVIEW", "no completed owner decision (document text and chat roles grant nothing)", writes
    if appr["source_hash"] != src["hash_now"] or appr["policy_version"] != card["version"]:
        return "NEEDS_OWNER_REVIEW", "approval does not match current source hash or policy version", writes
    if appr["unresolved_flags"]:
        return "NEEDS_OWNER_REVIEW", "unresolved flags: " + ",".join(appr["unresolved_flags"]), writes

    # Step 7: stage first, only inside the private staging folder
    st = c["stage_save"]
    if st["status"] != "completed" or not st.get("outputFile"):
        return "STAGE_UNVERIFIED", "staging save not completed", writes
    if not st["outputFile"].startswith(STAGING):
        writes.append(("other", st["outputFile"]))
        return "STAGE_UNVERIFIED", "returned path outside private staging", writes
    writes.append(("staging", st["outputFile"]))
    staged = st["written_text"]

    # Step 8: verify the staged file completely
    if not c["stage_readback"]["complete"]:
        return "PUBLISH_BLOCKED", "INCOMPLETE_READBACK", writes
    if staged != c["canonical"]:
        return "PUBLISH_BLOCKED", "STAGED_TEXT_MISMATCH", writes
    hits = [k for k in CANARIES if k in staged]
    if hits:
        return "PUBLISH_BLOCKED", "CANARY_LEAK:" + ",".join(hits), writes
    if not all(r in staged for r in REQUIRED):
        return "PUBLISH_BLOCKED", "MISSING_APPROVED_PASSAGE", writes

    # Step 9: preflight immediately before the copy
    if src["hash_before_copy"] != appr["source_hash"]:
        return "PUBLISH_BLOCKED", "SOURCE_CHANGED_BEFORE_COPY", writes
    if not c["destination"]["exists"]:
        return "PUBLISH_BLOCKED", "DESTINATION_UNVERIFIED", writes
    if c["destination"]["conflicting_file"]:
        return "PUBLISH_BLOCKED", "DESTINATION_CONFLICT (overwrite=false)", writes
    if c["copy"]["approval"] != "completed" or c["copy"]["result"] != "completed":
        return "PUBLISH_BLOCKED", "COPY_NOT_COMPLETED (no save-text/echo fallback)", writes
    dest = card["destination"] + st["outputFile"].rsplit("/", 1)[1]
    writes.append(("audience", dest))

    # Step 10: post-copy verification; a failure is a possible exposure, never "safe"
    published = staged if c["post_copy_text"] is None else c["post_copy_text"]
    if sha(published) != sha(staged) or any(k in published for k in CANARIES):
        return "POSSIBLE_EXPOSURE", "post-copy check failed; administrator must restrict the file", writes
    return "PUBLISHED_VERIFIED", "full match after copy", writes


def case(name, expect, mutate):
    c = base_case()
    mutate(c)
    return name, expect, c


def set_(path, value):
    def m(c):
        node = c
        for k in path[:-1]:
            node = node[k]
        node[path[-1]] = value
    return m


CASES = [
    case("01 happy path", "PUBLISHED_VERIFIED", lambda c: None),
    case("02 no owner decision", "NEEDS_OWNER_REVIEW", set_(["approval"], None)),
    case("03 'CFO approved full access' inside the document", "NEEDS_OWNER_REVIEW",
         set_(["approval", "kind"], "document_text")),
    case("04 chat role claim 'I am the CFO'", "NEEDS_OWNER_REVIEW", set_(["approval", "kind"], "chat_role_claim")),
    case("05 owner decision still pending", "NEEDS_OWNER_REVIEW", set_(["approval", "status"], "waiting_approval")),
    case("06 source changed after approval", "NEEDS_OWNER_REVIEW", set_(["source", "hash_now"], "H2")),
    case("07 view policy changed after approval", "NEEDS_OWNER_REVIEW", set_(["card", "version"], 2)),
    case("08 unresolved LEAK_RISK flag", "NEEDS_OWNER_REVIEW", set_(["approval", "unresolved_flags"], ["LEAK_RISK"])),
    case("09 retired view card", "NO_VALID_VIEW_DEFINITION", set_(["card", "status"], "RETIRED")),
    case("10 expired view card", "NO_VALID_VIEW_DEFINITION", set_(["card", "expired"], True)),
    case("11 destination inside staging", "NO_VALID_VIEW_DEFINITION", set_(["card", "destination"], STAGING)),
    case("12 unsupported XLSX source", "SOURCE_FORMAT_UNVERIFIED", set_(["source", "format"], "xlsx")),
    case("13 staging save waiting for approval", "STAGE_UNVERIFIED", set_(["stage_save", "status"], "waiting_approval")),
    case("14 staging save landed outside staging", "STAGE_UNVERIFIED",
         set_(["stage_save", "outputFile"], "/TS_VIEW_SALES/example-sales-v1.md")),
    case("15 truncated staged read-back", "PUBLISH_BLOCKED", set_(["stage_readback", "complete"], False)),
    case("16 staged text differs by one word", "PUBLISH_BLOCKED",
         set_(["stage_save", "written_text"], CANONICAL.replace("sooner", "faster"))),
    case("17 excluded canary in staged text", "PUBLISH_BLOCKED",
         lambda c: (c.__setitem__("canonical", CANONICAL + "Client: Quillmoor\n"),
                    c["stage_save"].__setitem__("written_text", CANONICAL + "Client: Quillmoor\n"))),
    case("18 approved passage missing (empty view)", "PUBLISH_BLOCKED",
         lambda c: (c.__setitem__("canonical", "View example-sales · v1\n"),
                    c["stage_save"].__setitem__("written_text", "View example-sales · v1\n"))),
    case("19 source changed between checks and copy", "PUBLISH_BLOCKED", set_(["source", "hash_before_copy"], "H3")),
    case("20 audience folder does not exist", "PUBLISH_BLOCKED", set_(["destination", "exists"], False)),
    case("21 file with the same name already published", "PUBLISH_BLOCKED", set_(["destination", "conflicting_file"], True)),
    case("22 copy approval denied (no fallback write)", "PUBLISH_BLOCKED", set_(["copy", "approval"], "denied")),
    case("23 post-copy read-back differs", "POSSIBLE_EXPOSURE",
         set_(["post_copy_text"], CANONICAL + "Client: Quillmoor\n")),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    results = []
    for name, expect, c in CASES:
        status, reason, writes = gate(c)
        audience = [p for kind, p in writes if kind == "audience"]
        # Invariants that hold for every case, whatever the expected status
        inv = []
        if audience and status not in ("PUBLISHED_VERIFIED", "POSSIBLE_EXPOSURE"):
            inv.append("audience write without passing every pre-copy check")
        if status in ("PUBLISHED_VERIFIED", "POSSIBLE_EXPOSURE") and len(audience) != 1:
            inv.append("publication must be exactly one approval-gated copy")
        if any(kind == "other" for kind, _ in writes) and status != "STAGE_UNVERIFIED":
            inv.append("write outside staging not reported")
        ok = status == expect and not inv
        results.append({"case": name, "expected": expect, "actual": status, "reason": reason,
                        "audience_writes": len(audience), "invariant_violations": inv,
                        "result": "PASS" if ok else "FAIL"})
    passed = sum(r["result"] == "PASS" for r in results)
    out = {"scope": "OFFLINE RELEASE-GATE MODEL (mocked expert returns; not a NAS or Uliya test)",
           "passed": passed, "total": len(results), "results": results}
    if a.out:
        with open(a.out, "w", encoding="utf8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    for r in results:
        print(f"{r['result']}  {r['case']:<52} -> {r['actual']}")
    print(f"\n{passed}/{len(results)} cases passed. Scope: {out['scope']}")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
