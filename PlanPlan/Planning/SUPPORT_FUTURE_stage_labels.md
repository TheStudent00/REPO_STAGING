# SUPPORT_FUTURE — stage labels: making brainstorms and future plans visible from the top

2026-08-12, ruled by the owner in conversation (PCv5 session; state record
`PseudoCoup_v5/DevComms/log_020_session_state_2026_08_12.md`
§5). This file is itself the first instance of the convention it
records — a `SUPPORT_FUTURE_` file, findable by filename glob from
any dashboard or sweep, changing nothing in PROTOCOL.md.

## The problem (the owner's statement)

Every folder can grow its own `.archive/`; brainstorms and future
plans land wherever they were born. Filed by LOCATION, ideas become
invisible from the top of a project — "a scattered mess of ideas" —
because location is the one thing scattered ideas do not share.

## What is adopted NOW (no protocol change)

- **Naming convention**: brainstorm and future-plan material goes in
  SUPPORT files named `SUPPORT_BRAINSTORM_<topic>.md` and
  `SUPPORT_FUTURE_<topic>.md`, placed beside the node they concern.
- why this shape won over a frontmatter `stage:` field, for now:
  - a CORE can simultaneously carry active design, a future
    extension, and a half-formed brainstorm; ONE file-level `stage`
    cannot say that. Per-file SUPPORT documents dissolve the
    multi-stage case: the CORE stays active by assumption, and each
    stage sits in its own co-located file.
  - sweepable by filename alone — a dashboard query is a glob for
    `SUPPORT_FUTURE_*` across trees, no frontmatter parsing.
  - inert where unused: absence of the convention means nothing,
    which matches the owner's "assumed active" default.
- `.archive/` stays exactly as it is (the owner): VCS is the ultimate
  archive; `.archive/` only tidies without burying things in the
  VCS timeline. It is NOT part of this labeling.

## Recorded as FUTURE (not to be built until the owner reopens it)

- a frontmatter `stage: brainstorm | future | active | archived`
  field (names undecided), orthogonal to `status`, inert when
  absent.
- a PROTOCOL.md amendment describing it.
- a check/projection extension: the sweep (`hq.sh check` /
  `generate_dashboards.py`) collects staged items by label and
  surfaces a centralized future-plans / brainstorms view in
  top-level DASHBOARDs — possibly subsuming this filename
  convention, possibly living beside it.
- open question noted at ruling time: whether DevComms logs enter
  the labeled world or stay a separate stream — the three-stores
  boundary (plan node / agent memory / DevComms log) is deliberate
  and this proposal must not blur it.
