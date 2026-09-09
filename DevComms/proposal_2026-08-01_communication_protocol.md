# Proposal — five additions to the communication protocol

2026-08-01. Written at the owner's request:

> considering the frustrations of the last few turns, what proposal
> for changes to the comms protocol would you make?

**ADOPTED IN FULL, 2026-08-01.** the owner: "there are proposals changes in
DevComms. i want those implemented also." All five are now live in
`~/Programming/DevComms/LLM_communication_protocol.md`:

| this proposal | where it landed |
|---|---|
| §1 quote the object | protocol §12a |
| §2 first sentence | protocol §9a |
| §3 a question's facts | protocol §15a |
| §4 a command as typed | protocol §14a |
| §5 one idea per bullet | a rule bullet inside protocol §5 |

The protocol is now the live text; this file is kept as the record of
what motivated each rule. Each item below names the failure that
motivates it, quoted, so the rule can be judged against the thing it
would have prevented.

One caveat first, stated because it bears on whether any of this is
worth adopting: §12 already requires claims to carry evidence, and §9
already requires the model before the conclusion. Both were in force
and both were broken. These additions are worth making only if the
sharper, more mechanical form binds where the general form did not.

---

## 1. Quote the object before characterizing it

The failure. Claude wrote:

> Roster entry removed — and it contradicted the hats rule sitting
> two nodes away, which says HQ can only request of PlanPlan.

Neither document appeared in the message. The characterization was
also false: the entry being described ended with

> not part of the line and not driven by HQ's commit script

so it stated its own exception and contradicted nothing. Quoting it
would have exposed that before the claim was made.

Proposed text:

```
## 12a. Quote the object, then characterize it

A claim about a file's content includes that content, in a `>` block,
with the file's path. A claim that two things conflict quotes BOTH
sides before naming the conflict.

Describing a document in your own words instead of showing it hides
whether you read it correctly. It also hides the disagreement from
me, which is the thing this protocol exists to make visible.
```

## 2. The first sentence rests on nothing later

The failure is the same sentence. `the hats rule` had never been
introduced, and the reader had to carry it to an explanation that
never arrived.

Proposed text:

```
## 9a. The first sentence rests on nothing later

The opening sentence of a message may not depend on a name, file, or
model introduced further down. If a summary line cannot be written
without one, the message does not start with a summary line.
```

## 3. A question states the facts it rests on

The failure. Claude asked the owner to resolve an inconsistency between two
repo lists without showing either list. the owner's reply:

> what? did i miss a decision here?

Proposed text:

```
## 15a. A question states the facts it rests on

Before asking me to decide, state what is true, where, in enough
detail that the question can be answered from the message alone. A
question I have to reconstruct context for is a question I cannot
check.
```

## 4. A command appears as it is typed

The failure. Claude referred repeatedly to `hq.sh check`. No such
command exists. the owner tried it:

> hq.sh check. idk what that is. ive tried running it in the
> terminal. doesnt work.

The runnable form is `bash ~/Programming/PseudoCoupHQ/hq.sh check`.

Proposed text:

```
## 14a. A command appears as it is typed

Reference a command in the exact form that runs it, including its
path. If a shorter form is being proposed, say that it does not exist
yet and give the line that would create it.
```

## 5. One idea per bullet

the owner, 2026-08-01:

> verbose is fine but typically sentences dont have to be extremely
> long. and each bullet point doesnt necessarily need more than one
> sentence. not strictly forbidden but often times completely
> unnecessary.

Proposed as an addition to §5 rather than a new section:

```
A bullet is one sentence unless a second sentence is load-bearing.
Length is not the problem; sentences that carry three clauses because
they were written as one thought are.
```
