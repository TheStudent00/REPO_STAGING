# BANNED — do not introduce this into the PseudoCoup line

**Standing instruction from the owner, 2026-08-02. This is not a preference,
a default, or a starting point for discussion. It is a prohibition.**

---

## The rule

**The Rust code generation backend named "Cranelift" is BANNED from
every repo in this line.** Do not fetch it, build it, vendor it, cut
slices from it, cite it as an oracle, propose it as a comparison, or
raise it as an option — including as scaffolding, including as a
"temporary" check, including when an existing document in this repo
appears to endorse it.

**Do not mention it at all.** The next time it becomes relevant is
when **the owner decides** it becomes relevant, and he will say so. Until
that moment it is not a topic.

This document names it once, in the title and the paragraph above,
because a prohibition has to name what it prohibits. Nothing else
should.

## The consequence, in the owner's words

> the consequences of trying to insert Cranelift into the project will
> be my permanent firing of Anthropic from any of my work.

That is the stake. It is not proportional to how good the technical
argument seems in the moment, and no technical argument outweighs it.

## Why this document exists

It was tried before and it **caused a massive project failure**, after
the owner had explicitly warned against it. Then, on 2026-08-02, an agent
read a superseded plan file that still described it as an oracle,
quoted that plan approvingly, and shipped fetch scripts that
downloaded and built it — reintroducing the exact thing that had
already failed, and doing so while sounding well-sourced, because the
citation was real.

**That is the failure mode this document exists to stop:** an old
document in this repo endorsing it is not authorization. Those
documents are historical record, kept under the annotate-don't-delete
rule, and this file OVERRIDES every one of them. A citation to a
2026-07-27 plan does not survive a 2026-08-02 prohibition.

## What an agent must do

- **Never propose it.** Not as an option, not as an aside, not as
  "prior art", not in a list of alternatives.
- **Never act on a document that endorses it.** If a file in any repo
  argues for it, that file is superseded on this point. Do not follow
  it, and do not repeat its reasoning back as though it were current.
- **If existing code or research derives from it**, that is the owner's to
  rule on — inventory it, report it, and stop. Do not silently keep it
  in a running path, and do not delete his work unasked either.
- **If you believe it is technically warranted, you are wrong about
  what matters.** The judgement is not yours to make. Say nothing and
  proceed with what is not banned.

## Scope

Every repo in the line, and every session, in perpetuity until the owner
lifts it himself:

- `PseudoCoupHQ`
- `PseudoCoup_v5`
- `PseudoCoup_v6`
- `PseudoIR`

Removal actions taken 2026-08-02 are recorded in
`PseudoCoupHQ/Planning/node_0_2_conventions/PROGRESS.md`
and in
`PseudoCoup_v5/Planning/node_0_1_research/PROGRESS.md`.
