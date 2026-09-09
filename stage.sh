#!/usr/bin/env bash
# stage.sh -- refresh REPO_STAGING from the live working repositories and
# commit-push the tip. REPO_STAGING exists to establish intellectual
# property under the OTU-GL: the authored methods (scripts, notes, designs,
# plans, logs) are the record; data produced BY those scripts is regenerable
# and stays untracked by .gitignore. History is never rewritten.
#
# The repository is PUBLIC, so the snapshot is SCRUBBED before it touches
# the tree: every source is copied into a private staging area
# (.stage_tmp/, gitignored), the patterns in scrub_patterns.tsv are applied
# there, a pattern that survives stops everything, and only then is the
# scrubbed copy mirrored into place. The tree therefore never holds an
# unscrubbed byte, not even for a second. The repo-daemon is configured to
# leave this repository alone; this script is the one way it changes.
#
#     bash ~/Programming/REPO_STAGING/stage.sh            # refresh, scrub, commit, push
#     bash ~/Programming/REPO_STAGING/stage.sh --no-push  # stop before the push
#
# A source that no longer exists on this machine is left as it is in the
# staging tree: its last snapshot stands as the record.
set -euo pipefail
cd "$(dirname "$0")"
PUSH=1; [ "${1:-}" = "--no-push" ] && PUSH=0
SOURCES=(PlanPlan PseudoCoupHQ PseudoCoup_v5 PseudoCoup_v6 PseudoIR DevComms)
TMP=.stage_tmp
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "== staging at $STAMP =="

# ---- 1. copy each source into the private area, tracked files only ---------
rm -rf "$TMP"; mkdir -p "$TMP"   # the private area starts empty every run
refreshed=()
for s in "${SOURCES[@]}"; do
    src="$HOME/Programming/$s"
    if [ ! -d "$src" ]; then echo "  $s: source absent here, staged copy left as is"; continue; fi
    mkdir -p "$TMP/$s"
    # only what the source repository TRACKS: the authored record, by the
    # source's own .gitignore; caches, virtual environments and generated
    # data never enter the snapshot
    git -C "$src" ls-files -z | rsync -a --delete --files-from=- --from0 "$src/" "$TMP/$s/"
    refreshed+=("$s")
    echo "  $s: copied ($(git -C "$src" rev-parse --short HEAD 2>/dev/null || echo 'no git') at source)"
done

# ---- 2. scrub the private area; refuse if anything survives ----------------
echo "== scrubbing =="
# text by extension first (file(1) misreads some sources as binary), then by mime
is_text() {
    case "$1" in *.md|*.py|*.sh|*.js|*.ts|*.txt|*.json|*.jsonl|*.tsv|*.csv|*.conf|*.cfg|*.ini|*.toml|*.yaml|*.yml|*.html|*.css|*.lean|*.c|*.h|*.cpp|*.hpp|*.rs|*.go|*.swift|*.java|*.php|*.rb|*.kt|*.dart|*.cs|*.tex|*.rst|*.log|*.sql|*.xml|*.svg|*.mmd|*.gitignore|Containerfile|Makefile) return 0 ;; esac
    case "$(file -b --mime-type "$1")" in text/*|application/json|application/x-shellscript|application/javascript) return 0 ;; *) return 1 ;; esac
}
scrubbed=0
while IFS=$'\t' read -r pat rep; do
    if [ -z "$pat" ]; then continue; fi
    case "$pat" in '#'*) continue ;; esac
    while IFS= read -r f; do
        if [ -f "$f" ] && is_text "$f"; then sed -i -E "s|$pat|$rep|g" "$f"; scrubbed=$((scrubbed+1)); fi
    done < <(grep -rlE -- "$pat" "$TMP" 2>/dev/null || true)
done < scrub_patterns.tsv
echo "  $scrubbed file-pattern replacements"
left=0
while IFS=$'\t' read -r pat rep; do
    if [ -z "$pat" ]; then continue; fi
    case "$pat" in '#'*) continue ;; esac
    # a survivor counts only if THIS repository would track it: a file its
    # own .gitignore excludes (generated data, build output) never enters the tip
    survivors=$( (grep -rlE -- "$pat" "$TMP" 2>/dev/null || true) | while IFS= read -r f; do if is_text "$f"; then echo "$f"; fi; done | sed "s|^$TMP/||" | (git check-ignore -v -n --stdin 2>/dev/null || true) | awk -F'\t' '$1 == "::" {print $2}' )
    n=$( [ -n "$survivors" ] && printf '%s\n' "$survivors" | wc -l || echo 0 )
    if [ "$n" -gt 0 ]; then echo "  STILL PRESENT after scrub (would be tracked): $pat in $n file(s):"; printf '%s\n' "$survivors" | head -5 | sed 's/^/      /'; left=$((left+n)); fi
done < scrub_patterns.tsv
if [ "$left" -gt 0 ]; then echo "  refusing: a pattern survived the scrub (a binary file, or a spelling the pattern misses). Nothing was placed in the tree."; exit 1; fi
echo "  clean: no pattern remains in the private area"

# ---- 3. mirror the scrubbed copy into the tree, then commit and push --------
for s in "${refreshed[@]}"; do
    rsync -a --delete "$TMP/$s/" "$s/"
done
git add -A
if git diff --cached --quiet; then echo "  nothing changed since the last staging"; exit 0; fi
n_files=$(git diff --cached --name-only | wc -l)
git commit -q -m "stage $STAMP: ${refreshed[*]} ($n_files files, scrubbed)"
echo "  committed: $(git log --oneline -1)"
if [ "$PUSH" = 1 ]; then git push -q origin "$(git rev-parse --abbrev-ref HEAD)" && echo "  pushed"; else echo "  not pushed (--no-push)"; fi
