---
id: pcv5.research.progress
status: living
---

# PROGRESS — research

- 2026-07-31: node founded, definition only.
- inherited and untouched: the pre-gutting research in
  `PRIVATE/PseudoCoup_v5/Research/` and `Designing/`. what
  survives the gutting is unsettled and is the owner's call.
- 2026-08-02 (the owner: "please modify the script to place the language
  source in `Sources`. that folder is filtered out from
  Timeshift"): **upstream language sources now live outside the repo**,
  in one shared root, so multi-hundred-MB checkouts are not carried
  into system snapshots. Three scripts changed, one cause:
  - `Research/rust_routing/fetch_sources.sh` — rust sparse checkout and
    `clif_probe`;
  - `Research/rust_routing/vendor_encoder.sh` — since DELETED under
    the prohibition recorded below;
  - `Research/llvm_trace/fetch_llvm.sh` — `llvm-project`, and its read
    of the rust checkout, which was a `../rust_routing/sources/rust`
    hop and is now the shared root directly.
  - Each sets `SRC="${PC_SOURCES:-$HOME/Programming/Sources}"`, so the
    default is the Timeshift-filtered folder and one env var overrides
    it for a machine laid out differently. `fetch_sources.sh` prints
    the root, and warns if the pre-move `sources/` folder is still
    present rather than silently fetching a second copy.
  - **Open, the owner's ruling 2026-08-02 — PCv6 is left broken meanwhile.**
    Four PCv6 files still resolve `$PCV5_ROOT/Research/*/sources/...`:
    `Tools/transpiler/test_llvm_encoder.py`,
    `Tools/ledgerer/test_ledger.py`,
    `Research/r2_compiler_source_census/census_sources.py`, and the
    path recorded in `AgentMemory/02_decisions.md`. They were already
    failing — the sources were never on disk and never committed — and
    they get fixed with the vendoring-into-PCv6 step that HQ's
    `node_0_0_projects/PROGRESS.md` already tracks as the unblocker.
- 2026-08-02 (the owner: "could you please create a single script that runs
  all three? also, i feel like PCHQ's hq.sh should be capable of doing
  that"): **one entry point for fetching upstream sources**, at
  `PRIVATE/PseudoCoup_v5/Research/fetch_all_sources.sh`, plus
  `bash PRIVATE/PseudoCoupHQ/hq.sh sources` which calls it.
  - Sequencing only, the rule hq.sh already follows: it calls the three
    fetchers, each of which still runs standalone. The order is
    load-bearing and stated in the file: `fetch_llvm.sh` adds sparse
    dirs to the `rust/` checkout `fetch_sources.sh` clones. (Written
    with three steps; reduced to two the same day — see the
    prohibition entry below.)
  - A failing step does NOT abort the run; failures are collected and
    reported at the end. A network failure on one checkout should not
    cost the other.
  - `--list` shows the root, the steps in order, and what is already
    present, fetching nothing and needing no network. `du` is behind
    `--sizes` rather than on by default: running it over the 2.3 GB
    llvm-project checkout exhausted the sandbox's system file table
    outright, and it is slow on the host for the same reason.
  - `hq.sh sources` is deliberately NOT part of the bare `hq.sh` run —
    a routine commit must never start a multi-hundred-MB network fetch.
  - **Verified**: `--list` and the argument guard run correctly against
    the real tree (it found the existing `llvm-project` checkout under
    `Sources`). hq.sh's dispatch was verified by the
    stub method the gate test already uses — a copy of hq.sh with only
    `SOURCES_SCRIPT` repointed at a stub: passthrough of `--list`,
    exit-code propagation from a failing step, and the missing-script
    branch all correct. **NOT exercised**: the real end-to-end fetch.
    It needs network and cargo, which the sandbox lacks; and nested
    execution of any script on the mount is currently failing there
    with ENFILE, which also affects the pre-existing
    `git_commit_push_all.sh` call, so it is the sandbox and not these
    scripts.

- 2026-08-02 **standing prohibition, the owner** — a Rust code generation
  backend is BANNED from every repo in this line. The authority is
  `PRIVATE/PseudoCoupHQ/CRANELIFT_IS_BANNED.md`, which names it;
  nothing else should. It had already caused a massive project failure
  after the owner explicitly warned against it.
  - **How it got back in, today:** an agent read
    `PRIVATE/PseudoCoup_v5/DevComms/plan_llvm_rust_2026-07-27.md`
    — a superseded plan that still describes it as an x86-64 oracle —
    quoted it approvingly, and shipped fetch scripts that downloaded
    and built it. The citation was real, which is exactly why it was
    persuasive and exactly why an old document endorsing it is not
    authorization.
  - **Removed the same day, in the fetch path:**
    `Research/rust_routing/fetch_sources.sh` lost the step that cloned
    and cargo-built it (it now fetches the rustc sparse checkout only,
    with `rustc_codegen_ssa` and `rustc_codegen_llvm` as the sparse
    dirs); `Research/rust_routing/vendor_encoder.sh` was DELETED, its
    entire purpose having been vendoring that backend's encoder;
    `Research/rust_routing/fetch_report.txt` deleted as that step's
    output; `Research/fetch_all_sources.sh` reduced from three steps
    to two; `Research/llvm_trace/check_resources.sh` no longer probes
    for its directory. Verified by grep: no script in `Research/`
    references it except as the prohibition.
  - **NOT removed, and awaiting the owner's ruling:** existing research
    material derived from it — `Research/vocab_transpiler/pc_vocab/`
    (23 files), `Research/rust_routing/slice_encoder.py`,
    `slice_lowering.py`, and the DevComms plans and handoffs that
    describe it. Deleting his research unasked is not the agent's
    call; the inventory was reported instead.

