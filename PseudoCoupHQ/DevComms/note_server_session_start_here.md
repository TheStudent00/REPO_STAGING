# Start here — instructions for the Claude session running on the tower guest

You are on a virtual machine hosted on a tower server. This folder is a
bundle: a complete copy of another machine's Airlock install, its container
images, its sandbox volumes, and the project directories its runs read. Your
job is to restore it, then run queued research lanes on it, because this
machine is much faster than the laptop the bundle came from.

Read this whole file before running anything. Then read, in this order:

1. `projects/Programming/DevComms/LLM_communication_protocol.md` — how to
   talk to the owner, the user. All of it. It is not optional and it is not
   generic advice; it is a specific contract with worked examples.
2. `projects/Programming/PseudoCoupHQ/CLAUDE.md` — the project's own rules.
3. `projects/Programming/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
   — the master plan, and §4.2 is the agreed work order.

---

## 1. Bringing the machine up

Run these in order, from this folder. Nothing here is destructive; every
step reports what it did.

```
bash prepare_host.sh --check     # reports; changes nothing
bash prepare_host.sh             # installs podman, git, rsync, python3; needs sudo
bash unpack.sh --verify          # every file's size against SIZES.txt
bash unpack.sh --cpus <N> --memory <N>g --up sandbox
```

- `--cpus` and `--memory` rewrite EVERY instance configuration at once. Use
  the guest's real numbers; the laptop's were small because it overheats and
  this machine does not. Leave a little headroom for the host.
- After `unpack.sh`, check with `<airlock>/airlock doctor` and
  `bash <airlock>/selftest.sh`. Seven checks should pass.
- If `prepare_host.sh --check` does not list `cpu` among the delegated
  controllers after a fresh login, container processor caps are silently
  ignored. Fix that before running anything long.

Where things land, with `<home>` the guest user's home directory:

| what | path |
|---|---|
| the tool | `<home>/Programming/Airlock` — call it `<airlock>` below |
| the research repo | `<home>/Programming/PseudoCoupHQ` |
| research artifacts | `<home>/Programming/PseudoCoupHQ/Research/op_pipeline` and `Research/oracle` |
| the planning tree | `<home>/Programming/PseudoCoupHQ/Planning` |
| written reports | `<home>/Programming/PseudoCoupHQ/DevComms/log_<nnn>_<task>_<topic>.md` |
| an instance's run record | `<home>/AirlockRuns/<instance>/agent/{drop,status,logs,out}` |
| the default instance's run record | `<airlock>/agent/{drop,status,logs,out}` |

## 2. The standing rules. These bind every session on this line

- **All compute runs through Airlock.** Never run analysis on the guest
  directly, never create a Python virtual environment outside the image. A
  missing tool is installed INTO the image by editing
  `<airlock>/Containerfile` and rebuilding, never worked around.
- **One instance per task.** Copy `<airlock>/instances/t97.conf` to
  `<task>.conf` and state the reason for every number in the header. Bring
  the instance down when the task is done.
- **Lane scripts are kept in the repo.** Write each lane first under the
  task's artifact folder as `lanes_<task>/<lane name>.sh`, submit it from
  there. Airlock's own `.done` archive is not the record.
- **Never delete anything under `<airlock>/` or `<home>/AirlockRuns/`.**
- **Never end a turn while a lane you need is still running.** No
  notification arrives when a lane finishes. Poll in a bounded loop inside
  one call: `timeout 3500 bash -c 'until <airlock>/airlock --instance <t>
  status | grep -q done; do sleep 60; done'`, repeated as needed.
- **State a memory bound for any big-data lane**, sample first, paste peak
  resident size from `resource.getrusage`, and abort at the stated ceiling
  with a named outcome. `/usr/bin/time` is absent from the image.
- **A time or memory limit is a flag, not an answer.** Re-run with more
  room and report whether the answer changed. Never change what is measured
  to fit a limit.
- **Every claim in a report carries the command that reproduces it**, and
  the final lane of every task runs
  `check_conventions_log_claims.py --verify --timeout 20 <log>` from that
  task's own instance. Paste the tally. Zero DIFFERS. Fix the log or the
  claim, never the verifier.
- **The spelling ban.** No operator token — `+`, `>>`, `&&` and the like —
  may appear in any key, grouping, pairing, row structure, candidate
  selection or comparison scope, anywhere in this line. Candidates for
  comparison come from machine-form evidence or from ratified intention,
  never from the token. The token appears once per unit, as a display label.
  Every stage that groups or pairs units runs
  `Research/op_pipeline/check_no_spelling_keys.py` over its own output and
  refuses on failure. That guard file is never modified.
- **Vocabulary.** Never a socio-familial word for an object relationship:
  use super and sub, co-objects, super-chain, sub-tree, unlinked. Never a
  death word for a process: a run is stopped or aborted, and the outcome
  label is ABORT.

## 3. What the work is

The research line studies arch-units: one function body's machine code plus
the facts about where its arguments arrive and where its answer goes. The
branch that is live is arch-opcode emulation, and the owner's own framing of it is
this loop, in his words:

```
for arch_opcode_i in set_of_unique_arch_opcodes:
    for lang_i in set_of_languages:
        emulated_arch_opcode = find_emulation(arch_opcode_i)
```

| his name | what holds it |
|---|---|
| `set_of_unique_arch_opcodes` | `Research/oracle/arch_opcodes/unique_opcodes.json`, 162 mnemonics |
| `set_of_arch_units_for_each_lang` | the canon stores under `Research/op_pipeline` |
| `set_of_singletons_for_each_lang` | `Research/oracle/arch_opcodes/single_opcode_units.json` |
| `set_of_emulated_unique_arch_opcodes_for_each_lang` | tasks o8 and o11: 25 of 162 opcodes, targets c and rust only |

The model of one opcode is a primitive plus its edge regions, not a lookup
table: the language operator that is effectively the opcode, the region of
inputs where the two agree, the regions where they differ, and the control
flow that routes between them. The goal section of
`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`
states it; `DevComms/log_234_arch_opcode_mappings_as_fits.md` records the
study of how compressible each opcode's mapping is.

**The queue, in order.** Do not start any of it without the owner saying so.

1. The 162-row model table, read out of `Research/op_pipeline/reference.py`:
   per mnemonic and operand width, the mapping, the flags written, the fault
   region. Definition work over existing code, no proofs.
2. The missing `find_emulation` printers: go and swift, after the existing c
   and rust ones in `Research/oracle/cross_construction/emulation/`.
3. The loop over all 162 opcodes and every compiled language, with the
   existing check: render, compile at ship flags, carve, gate.
4. A check for the interpreted languages, which have nothing to carve.

## 4. Reporting back

The bundle carried each repository's history, so `git log` works and you can
commit locally. It did NOT carry credentials, so pushing will fail until
the owner adds them. Until then:

- commit locally after every meaningful change, as the laptop does;
- write every report as a DevComms log with the next free number, checking
  `ls <repo>/DevComms | tail` immediately before writing so two sessions do
  not collide;
- tell the owner in chat what changed and where, in the form the protocol
  requires: the walkthrough first, then the evidence.

## 5. What not to do

- Do not modify, clone or rename Airlock to get a second sandbox. A second
  sandbox is an instance: one configuration file and a flag.
- Do not use sub-agents for a task brief that says to do the work yourself.
- Do not treat a subagent's or a tool's summary as evidence. Read the
  artifact.
- Do not answer a question about this line's numbers from memory. Every
  figure carries what it counts and when it was measured.
