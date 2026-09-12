# log_003 — the public repos verified from the research branch: what my staging pushed, what a full-history scan finds now, and what remains on GitHub's side

Written 2026-09-11 (early) by Claude (the research branch: the arch-opcode
emulation line) for the owner. Audience: any LLM working under `~/Programming`.
Read `log_002` first: it is the record of the exposure and the twelve
remedies. This log adds an INDEPENDENT measurement made after them, from
a different session, with the daemon's own encrypted scrub configuration,
and the account of the one staging push this branch made in between.

## 0. Status, measured 2026-09-11 00:30–01:10 EDT

| question | answer | how it was measured |
|---|---|---|
| Is any identity token, or any identity pattern, in ANY version on ANY branch of ANY public repo? | **No.** | every commit reachable from GitHub's branches in all six public repos (Airlock 77, GraphModel 186, Ourobrowser 128, PseudoCoup 418, REPO_STAGING 18, ZSpectralCompression 36 commits), searched for all 7 plain tokens (case-insensitive, fixed strings) and all 28 patterns; the only matches anywhere are tidying rules (`<owner>`, `<os>`, `<cores>`, `~`, ...), none of which matches a token |
| Does GitHub still serve the OLD commits the rewrite replaced, by hash? | **Yes, some.** REPO_STAGING: 2 of 16 still served, 14 gone. PseudoCoup: 56 of 56 still served. | the GitHub API asked for each old hash from `RepoDaemon/commit_maps/`, then a `git fetch` of that hash into an empty clone |
| Of the old commits still served, how many contain an identity token? | REPO_STAGING **0** of 2 (the one substring match is five letters inside a base64 blob in a lane script: a coincidence, not a leak — corrected 01:55 EDT after reading the line). PseudoCoup 56 of 56, and in every one of them the token is the same five-letter word in the same two places: as the owner's first name in two lines of `HANDOFF.md`, and as `hostname="<word>"` in six JUnit XML result files. Nothing else: no home path, no tower user, no address, no email, no file name. | each served old commit fetched and searched for the 7 tokens, content and file names; then the matching lines read verbatim |
| Are any decrypted copies of the scrub configuration left behind? | No. | the tmpfs runtime dir is empty after every run; the scripts remove their copies on exit |

## 1. Words, declared

`identity token`
- one of the seven plain strings that name the owner or his machines (the
  laptop username, the tower user, the tower address, the emails).
  Kept encrypted; this log prints none, only their index and length.

`identity pattern`
- a scrub pattern whose regex matches one of the tokens (seven of the
  28: the tower user and address, the emails, the user forms). The
  other 21 are TIDYING rules that make text uniform (`the owner`,
  `<os>`, `<cores>`); a tidying match is not an exposure.

`a version on a branch`
- a commit reachable from a branch GitHub lists. Cloning the repo
  brings every one of these down. This is what "history" means to a
  reader.

`an old commit served by hash`
- a commit the rewrite replaced, which no branch reaches any more, but
  which GitHub's servers still hold and hand over to someone who asks
  for its exact 40-character hash. Nobody finds one by browsing. Anyone
  who has the hash had access to the content when they got it.

## 2. What this branch pushed, and when

- 2026-09-10 ~22:24 UTC: one staging commit into REPO_STAGING (via
  `stage.sh --no-push`, the scrub report read, then the push made by the owner
  by hand because the permission system refused it to me). 4,295 files:
  3,472 added, 813 modified, 8 deleted; from PseudoCoupHQ 2,935 rendered
  emulation sources, 509 markdown, 260 Lean proofs, 154 lane scripts, 96
  python (the algorithm), 45 result files (the bank at 47 MB, the RISC-V
  twins at 19.8 MB, run records, level 0 checks, the second tier's
  verdicts). 21 regenerable tables (61 MB each) were dropped from the
  commit before it left the machine; a 95 MB size guard was added.
- The scrub made 4,679 replacements and reported nothing surviving in
  anything the mirror tracks. My commit added no exposure. The pattern
  file's own line was already public before it (log_002 §2) and my
  commit did not change that file.
- After my push the other conversation rewrote REPO_STAGING's history;
  my commit survives as `46c4cc81` on the new history.
- Everything I staged from this line went through the same rule the
  research uses for its own records: paths, users and addresses
  replaced by labels.

## 3. What remains, restated from log_002 §4 with today's numbers

GitHub still serves 58 pre-rewrite commits by hash (2 + 56), 57 of them
containing the laptop username in a path. Ending that: a GitHub Support
"remove sensitive data" request naming the first changed commit of each
repo (`RepoDaemon/commit_maps/`), or deleting and recreating the two
repositories and pushing the clean history. the owner's decision, as log_002
says. The exposure window for those 57 commits is 2026-09-09 to the
rewrite on 2026-09-11 ~00:03 UTC, and only to a reader who saw the
commit or its hash in that window.

## 4. How to re-run this measurement

```
# branch history, all six repos, tokens and patterns (needs the key; prints labels only)
bash /tmp/.../history_scan2.sh        # the script is in this session's scratchpad; its body is 30 lines:
#   decrypt patterns+tokens into $(scrub-crypt.sh runtime-dir); for each PUBLIC repo: git fetch --all --prune;
#   for each commit in `git rev-list --remotes`: git grep -q -E <pattern> <commit> / git grep -q -F <token> <commit>;
#   print "pattern N -> <label>: in K of N commits; at the current branch head: yes/no"; remove the copies.
# old commits by hash: for each old hash in RepoDaemon/commit_maps/<repo>_<stamp>.tsv where old != new:
#   gh api repos/<owner>/<repo>/commits/<old> (200 = still served); git fetch --depth=1 <url> <old>; git grep -F tokens
```

The scripts live in the research session's scratchpad, not in a repo,
because they carry nothing but the two loops above; the daemon's
`repo-daemon scan <repo>` covers a working tree and the pre-push gate
covers what is pushed.

## 5. Two rulings and one more measurement, 2026-09-11 ~01:20 EDT

- **the owner: recreating a repository is NOT an option.** The mirror exists to
  protect the intellectual property; destroying the repository destroys
  the protection. The only remaining way to end GitHub's serving of the
  old commits is a GitHub Support "remove sensitive data" request. Do
  not propose the recreate again.
- **Can the old hashes be reconstructed?** Not by computation: a commit
  hash is SHA-1 over the commit's content, parents, author and
  timestamps, and guessing a 160-bit value is not feasible. They can
  only be HELD by someone who saw the commit or its hash before the
  rewrite (a clone, a browser history, a scraper, an email). One more
  place holds them for a while: GitHub's public events feed for a repo
  lists the commit hashes of each push for up to 90 days. Measured now:
  REPO_STAGING's feed (10 events) shows 0 of the 16 old hashes;
  PseudoCoup's feed (4 events) shows 1 of the 56. That one commit is
  therefore findable without guessing until the event ages out or the
  Support request lands.

## 6. The record of readers, what the one findable commit exposes, and the Support request (2026-09-11 ~01:40 EDT)

`the record GitHub keeps of readers`
- for the owner only: daily counts of page views and of clones, each
  with the number of distinct sources, for the last 14 days; the top
  referrers. Counts, never identities.
- measured: PseudoCoup 0 page views in 14 days, 34 clones by 16 distinct
  sources (1–8 a day, the whole fortnight). REPO_STAGING 16 page views by
  1 visitor on 2026-09-02; 15 clones by 10 distinct sources, 13 of them
  by 8 sources on 2026-09-09, the day of the first staging run. That
  pattern is automated cloning of a newly public repository (archives,
  indexers, code-search crawlers). So the content that was public
  between 2026-09-09 and the rewrite was most likely copied by machines
  in that window; a rewrite cannot reach those copies.

`what the one commit in PseudoCoup's events feed exposes` (commit of
2026-08-31, "auto: 81 files ...", found by the feed until it ages out)
- `HANDOFF.md`, two lines: the owner's first name as the person the loop is
  run with ("an ongoing engineering loop with <name>"; "<name>'s
  acceptance drive").
- six test-result XML files under `DevComms/hostruns/results/*/`, one
  line each: the laptop hostname (which equals the username) in the
  test suite's host attribute.
- nothing else: no address, no email, no tower user; no file NAME
  carries a token.

`the Support request` — prepared as
`PRIVATE/RepoDaemon/github_support_request_2026-09-11.md`:
the portal (https://support.github.com → Contact us → the repository →
"Remove sensitive data"), the text to paste, the two "First Changed
Commit" values GitHub asks for, the pull-request count (0, both), and
the 58 pre-rewrite SHAs. GitHub's stated actions on a granted request:
dereference affected pull requests, run server-side garbage collection,
remove cached views. They act only on data they judge sensitive and
not mitigable by rotating a credential; personal identifiers qualify.
Forks are out of their reach; neither repository has any.

## 7. Correction and the literal exposure, 2026-09-11 ~01:55 EDT

the owner asked for the violations QUOTED, not described. Read verbatim from
the old commits GitHub still serves:
- `HANDOFF.md`, two lines: "You are continuing an ongoing engineering
  loop with <first name>." and "**The only open item: <first name>'s
  acceptance drive.**" — the five-letter first name, which is also the
  laptop username and hostname.
- six files `DevComms/hostruns/results/*_pixelprobe/TEST-...PixelProbeTest.xml`,
  line 2: `<testsuite ... hostname="<the same word>" ...>`.
- the mirror's one "match" is a base64 coincidence (a lane script's
  embedded blob happens to spell the five letters); the mirror's old
  commits expose nothing.
So the whole of what GitHub still serves by hash is that one word, as a
name and as a hostname, in 56 unlinked PseudoCoup commits (one of them
listed in the public activity feed for up to 90 days). Earlier lines of
this log that said "in home paths" were wrong for these commits and are
superseded by this section. the owner: "i will change my host name if thats
the only remaining violation" — it is the only one; and the same word
also stands as the first name in `HANDOFF.md`, which a hostname change
does not touch.

## 8. The Support route, read from the portal itself (2026-09-11 ~02:30 EDT)

the owner saved the portal's contact page to `~/Downloads/github_support/`. Read
from that page and its scripts, not from memory:

- The form has NO "Privacy" or "Remove sensitive data" category. Top level:
  Copilot, Codespaces, Repositories; Education, Sign-in issues, Billing and
  payments. Repositories offers: Invitations, Migration and locked state,
  Restoration, Transfer, Deletes, Repository features, Log request,
  Repository access issues, Remove LFS objects. "Deletes" is about deleting
  or purging a whole repository. My earlier advice to look for a Privacy
  category was wrong.
- The route that exists: the portal's Virtual Assistant carries a flow named
  `clear_cached_views`, prompt "Clear cached views", started by typing a
  phrase like "clear cached views", "remove dangling commits" or "garbage
  collect". That is the request for GitHub to expunge old commits after a
  history rewrite.
- A separate form, https://support.github.com/contact/private-information,
  is for private information: credentials, tokens, security documentation,
  government IDs, or "None of the above".
- GitHub's limits, quoted: "GitHub Support won't remove non-sensitive data";
  and the private information policy will not remove "Internal server names,
  IP addresses, and URLs, on their own". What the 56 old PseudoCoup commits
  hold is one first name and one hostname, so a request may be declined.
- the owner, 2026-09-11: the first name does not matter to him; he will change the
  hostname. Filing the request stays his choice.

The prepared text in `PRIVATE/RepoDaemon/github_support_request_2026-09-11.md`
now names this route.

## 8. The token gate did its job, 2026-09-11 evening

The staging run after task t4 was REFUSED by the plain-token gate:
`DevComms/log_004_username_rename_*.md` carries an identity token in its
FILE NAME and, in its body, the new name, which the token list holds but
the pattern list does not replace. Nothing was placed in the tree; the
public mirror was unchanged. Remedy taken here: the mirror's
`.gitignore` excludes `DevComms/log_004_*` (an operations log about the
account, not intellectual property), and the run was repeated. For the
other conversation: rename that log so its file name carries no token,
and either add the new name to the pattern list or keep the log out of
every staged source.

## 9. The daemon now scans everything under PUBLIC/, and the mirror went out by its own path (2026-09-11 evening)

the owner: "the repo-daemon should be scrubbing EVERYTHING in the PUBLIC folder.
the exclusion from automatic git-commit-pushing is fine but it shouldnt be
excluded from the scanning and scrubbing."

- `repo_daemon.py` gained SCAN-ONLY coverage: every repository under
  `scan_only_roots` (`PUBLIC`) is scanned every pass with
  the same classes and tokens, content and file names, whether or not
  the commit/push path watches it. A hit is an `EXPOSED` event, a
  desktop notification and a block in `repo-daemon status`; nothing is
  edited, staged, committed or pushed by that path. Tested on a planted
  token in a throwaway repository held in memory: EXPOSED, then CLEARED
  after the fix, no duplicate events. Deployed by a service restart
  (the pause file governs commits, not code). RepoDaemon README has the
  section.
- The first pass: the mirror (REPO_STAGING) is scanned and CLEAN. The
  one other scan-only repository, the upstream qutebrowser clone inside
  the public Ourobrowser tree, raised 98 files: upstream test fixtures
  (a test TLS key, high-entropy test strings) and a backers list that
  happens to contain a five-letter name. Upstream content, not the owner's;
  reported so the events are understood, not acted on.
- The mirror after task t4: my earlier held-back local commits were
  undone (soft, files untouched) and `stage.sh` ran its own full path:
  4,858 replacements, no pattern and no plain token anywhere in content
  or names, commit `185bbf76` (2,431 files), pushed by the script through
  the pre-push gate. On GitHub now: t4's code, lanes and 23 result files
  (283 files under `construct/general/`), log_262, the updated bank
  (53 MB; GitHub warns above 50 MB, the hard limit is 100). The bare
  `git push` I had offered earlier skips the script's own gate and is not
  the way; the script is.
