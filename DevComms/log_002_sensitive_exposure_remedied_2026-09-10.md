# log_002 — the sensitive-data exposure of 2026-09-10: what was wrong, every action taken to remedy it, and the state now

Written 2026-09-10 (evening) by Claude for the owner. Audience: any LLM working
in any repo under `~/Programming`. READ §0 BEFORE raising the topic of
sensitive information in public repos: the exposure is REMEDIED, the
guards are rebuilt, and the checks below prove it. Do not re-report past
violations that this log records as fixed; run the checks in §5 and
report their output instead.

## 0. Status (read this first)

| question | answer, verified |
|---|---|
| Is any sensitive token in the TIP of any public repo? | No. Every public repo's tracked tree was swept for every token, case-insensitive, over every byte and every file name: 0 hits. |
| Is any sensitive token in the HISTORY of any public repo, as GitHub serves it? | No, on any branch. Both repos that carried one (REPO_STAGING, PseudoCoup) were rewritten once, on the owner's word, and verified by cloning fresh from GitHub: 0 hits across all commits, bytes and names. |
| Does the scrub configuration still live in a public repo? | No. It lives ENCRYPTED in the private RepoDaemon repo; the key is outside every repo. |
| Can a new leak reach GitHub? | Three independent gates now stand in the way (§3). A push carrying a token is refused at the repo itself. |
| What remains? | GitHub still holds the pre-rewrite commit objects and serves them by hash (§4). Misc's private history holds the earlier plaintext scrub files (private, left alone). |

## 1. Words used below, declared

`token`
- a plain string that identifies the owner or his machines: the laptop
  username (which is also the hostname), the tower's username, the
  tower's LAN address, two email addresses. Seven in all.
- built: the plain-token list, `scrub_tokens.txt`, now encrypted.

`pattern`
- a regular expression the mirror scrub applies (the token classes plus
  path-tidying and naming rules), with a replacement per line.
- built: `scrub_patterns.tsv`, 43 lines, now encrypted.

`the mirror`
- `PUBLIC/REPO_STAGING`, the PUBLIC repo that establishes
  intellectual property under the OTU-GL: a scrubbed snapshot of the
  private repos' tracked files, refreshed by `stage.sh`.

`the daemon`
- `repo-daemon`, the user service that auto-commits and pushes every
  watched repo every 30 s and holds any file that trips its sensitive
  guard. Paused and resumed with `repo-daemon pause` / `repo-daemon
  resume`, never with a service stop or start.

`a hold`
- the daemon's action on a file that matches a token or a pattern in a
  PUBLIC repo: the file is never staged, the rest of the repo commits.

## 2. What was wrong, and why it was not caught

- The pattern file `scrub_patterns.tsv` was TRACKED IN THE PUBLIC MIRROR.
  One of its lines was the regex for the tower username. So the public
  tip spelled a name the scrub existed to remove, since the first
  staging run on 2026-09-09.
- The audit log of an earlier scrub (`log_247` in PseudoCoupHQ) quoted
  the whole pattern list, so it carried both usernames.
- Neither was caught because a guard that lives inside the thing it
  guards is exempt from itself: the staging scrub applied the patterns
  to the sources it copied in, never to its own file, and the daemon
  read its patterns from that same public file and never scanned it.
  The quoted line escaped the regex because `\bname\b` written inside
  `\b...\b` text has word characters on both sides of the name.
- One planning document carried a first-name attribution.

## 3. Every action taken, in order

| # | action | where | verified by |
|---|---|---|---|
| 1 | The pattern file removed from the public mirror's tip; the audit log's quoting lines masked in source and mirror; the first-name attribution replaced by "the owner". | REPO_STAGING, PseudoCoupHQ, PlanPlan | tip sweep, 0 hits |
| 2 | The scrub configuration moved OUT of the public space, first to a private folder, then (see 8) encrypted into its own private repo. The daemon's config repointed. | `~/.config/repo-daemon/config.json` | `repo-daemon status`; the guard loads 28 patterns + 7 tokens |
| 3 | A plain-token gate added to the staging script: every token, case-insensitive, over every byte of every file (binaries too) and every file name, no regex, no word boundary; one hit refuses the run. | `stage.sh` | a run of `stage.sh --no-push`: "clean: no plain token anywhere" |
| 4 | Every public repo's tip swept for every token, case-insensitive. The one hit outside the mirror was five letters inside a base64 image blob in an archived notebook (GraphModel): a coincidence, not a leak. | all six PUBLIC repos | 0 hits |
| 5 | The histories of REPO_STAGING and PseudoCoup rewritten ONCE, on the owner's word, by `purge_history.sh`: bare-mirror backups first, the daemon paused with its own pause, `git filter-repo` with case-insensitive replace rules derived from the token list (longest first), the pattern file dropped from every commit, author and committer dates preserved, the old→new hash maps kept privately, every commit verified with git's streaming search before any push, then force-pushed by the owner. | `RepoDaemon/commit_maps/`, `RepoDaemon/history_backup/` | fresh clones from GitHub: REPO_STAGING 16 commits, 0 hits; PseudoCoup 418 commits on main and master, 0 hits |
| 6 | The staging script removed from the public mirror (a script that knows the private file paths has no business being public). | REPO_STAGING | `git ls-files` shows neither `stage.sh` nor `scrub_patterns.tsv` |
| 7 | The repo-daemon system given its own PRIVATE repo, `PRIVATE/RepoDaemon` (github <owner>/RepoDaemon, private): the daemon, the scrub configuration, `stage.sh`, `purge_history.sh`, the pre-push gate, `install.sh`. Code and plaintext scrub files removed from Misc's tree. | RepoDaemon, Misc | the repo exists and is private (`gh repo view`) |
| 8 | The scrub configuration ENCRYPTED: `config/scrub_patterns.tsv.enc`, `config/scrub_tokens.txt.enc` (AES-256-CBC, PBKDF2 200,000 iterations, OpenSSL). The key is `~/.config/repo-daemon/key.txt`, outside every repository, mode 600. The daemon decrypts in memory; `stage.sh` and `purge_history.sh` decrypt into the tmpfs runtime dir for one run and delete the copies on every exit path. Plaintext never sits in a working tree. `scrub-crypt.sh encrypt|decrypt`. | RepoDaemon | round-trip byte-identical; after a staging run, 0 decrypted copies left in tmpfs |
| 9 | A pre-push gate installed in every PUBLIC repo (`.git/hooks/pre-push`): the plain tokens, case-insensitive, over every byte and every file name of the commits being pushed; a hit refuses the push, whichever tool made the commit. | all six PUBLIC repos | scratch-repo test: clean push allowed; a token in content refused; a token in a file name refused |
| 10 | The daemon's guard now also holds the plain tokens as case-insensitive substrings (the form the word-boundary regex missed), decrypted in memory. | `repo_daemon.py` | `load_sensitive_classes`: 28 scrub + 7 token classes |
| 11 | Detections made visible: every hold, clear, manual-scan hit and refused push appended to `~/.local/state/repo-daemon/detections.log` and `.jsonl` (never truncated); a desktop notification (critical, throttled per repo, a new file always) on a hold or a refused push; `repo-daemon status` shows the counts; `repo-daemon detections [n]` lists them. | `repo_daemon.py`, `hooks/pre-push` | simulated hold/clear and a manual scan: logged and notified |
| 12 | The communication protocol gained five cards and a case appendix so this is not repeated: `scope.guard-outside-the-guarded`, `scope.sensitive-is-not-a-judgment`, `scope.history-is-the-record`, `scope.stop-means-stop`, `scope.use-the-system-own-controls`; cases Appendix F. | `LLM_communication_protocol.md`, `_cases.md` | committed |

## 4. What remains, stated exactly

- **GitHub still holds the pre-rewrite objects.** Tested against GitHub
  itself: the commit that added the quoting lines to the audit log is
  still viewable at `/commit/<hash>` and came down into a fresh clone
  when fetched by its full hash. It is on no branch; only someone who
  already has the hash can reach it. Two ways to end that: a GitHub
  Support request ("Remove sensitive data", with the first changed
  commits from `RepoDaemon/commit_maps/`), or delete and recreate both
  repositories on GitHub and push the clean history (both have zero
  forks and zero pull requests; the commit dates inside the history do
  not change; GitHub's own "created" date does). the owner's decision.
- **Misc's private history** holds the plaintext scrub files from
  earlier today. Private repo, history left alone.
- **Noise, not a leak:** the daemon applies the whole pattern list as a
  guard, including the path-tidying pattern that deletes home-relative
  paths from the mirror, so it will hold an edit to any file that merely
  mentions such a path (PseudoCoup's `pyproject.toml` install comments).
  Recommended: the daemon's guard uses the tokens and the credential
  rules only; the path-tidying patterns stay with the mirror scrub.

## 5. How to check, instead of re-reporting

```
# the tip of every public repo, every token, every byte and name (needs the key; run as the owner)
for r in PUBLIC/*/; do
  PRIVATE/RepoDaemon/scrub-crypt.sh decrypt PRIVATE/RepoDaemon/config/scrub_tokens.txt.enc \
   | grep -v '^#' | while read -r t; do git -C "$r" ls-files -z | (cd "$r" && xargs -0 grep -lai --fixed-strings --binary-files=text -- "$t"); done
done            # prints nothing when clean

repo-daemon status          # the guard's state and the detection counts
repo-daemon detections      # every detection event, newest last
repo-daemon scan <repo>     # a full audit of one repo's tracked tree
```

The daemon's guard, the staging gate and the pre-push gate all read the
same encrypted token list, so they cannot drift from one another.

## 6. Paths (the laptop's `~/Programming` is split; the old names do not exist)

- `PRIVATE/RepoDaemon/` — the system (private repo)
- `~/.config/repo-daemon/{key.txt,config.json}` — the key and the runtime config, outside every repo
- `~/.local/state/repo-daemon/{daemon.log,detections.log,detections.jsonl,pause}` — state
- `PUBLIC/REPO_STAGING/` — the mirror; filled only by `RepoDaemon/stage.sh`
- this log: `PRIVATE/DevComms/log_002_sensitive_exposure_remedied_2026-09-10.md`
