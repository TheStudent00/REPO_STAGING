# task 58 resume state

Written before the work and updated during it.  Home:
`PRIVATE/PseudoCoupHQ/Research/op_pipeline`.

## nothing is part-done

`gate58_store/` holds 332 files, one per canon38 source document
(5 original languages + the interpreter + 326 regenerated chunks), and
every one of the 30,436 units task 52 proved has a record in it.  Each
of the six shard logs ends `shard N/6 finished`.

## how to re-run, in order

All five run under `/tmp/reconnect_venv/bin/python3`.

1. `gate58_run.py --shard=0/6` .. `--shard=5/6` -- the re-gate.  A
   shard skips any source whose output file already exists, so an
   interrupted lap resumes by running the same command again.  For a
   full redo, delete `gate58_store/`.  Whole corpus: about 21 seconds
   with six shards on this machine.
2. `audit58.py > audit58_printed.txt` -- the figures and
   `audit58.json`.
3. `acceptance58.py > acceptance58_printed.txt` -- the instances and
   `acceptance58.json`.
4. `guard58.py` -- LAST, because it walks every file steps 1-3 wrote.

Steps 2-4 are read-only over step 1's artifacts and are re-runnable at
any time.

## what the next task reads

`gate58_store/*.json`.  Each unit record carries `unit`, `lang`,
`population`, `term_built`, `transcription_refused`, and the two
verdicts `ship` and `text`, each a `Verdict` as a mapping (`outcome`,
`reason`, `counterexample`, `route`, `solver_timeout_ms`).

The proved population for the pool's merge grounds is the **25,179**
units whose record has `term_built` true, no `DISPROVED` outcome, and
at least one `PROVED_ON_SHIP` -- the reading `audit58.py`'s
`state_after` applies.
