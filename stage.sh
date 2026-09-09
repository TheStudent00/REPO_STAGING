#!/usr/bin/env bash
# stage.sh -- refresh REPO_STAGING from the live working repositories and
# commit-push the tip. REPO_STAGING exists to establish intellectual
# property: the authored methods (scripts, notes, designs, plans, logs) are
# the record; data produced BY those scripts is regenerable and stays
# untracked by .gitignore. History is never rewritten.
#
# The repo-daemon does not cover this repository (it holds copies, not a
# working tree), so this script is the one way it is updated:
#
#     bash ~/Programming/REPO_STAGING/stage.sh            # refresh, commit, push
#     bash ~/Programming/REPO_STAGING/stage.sh --no-push  # refresh and commit only
#
# Each source is copied with rsync, its own .git excluded, deletions
# mirrored (the tip is a snapshot; earlier commits keep what they held).
# A source that no longer exists on this machine is left as it is in the
# staging tree, untouched: its last snapshot stands as the record.
set -euo pipefail
cd "$(dirname "$0")"
PUSH=1; [ "${1:-}" = "--no-push" ] && PUSH=0

SOURCES=(PlanPlan PseudoCoupHQ PseudoCoup_v5 PseudoCoup_v6 PseudoIR DevComms)
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "== staging at $STAMP =="
refreshed=()
for s in "${SOURCES[@]}"; do
    src="$HOME/Programming/$s"
    if [ ! -d "$src" ]; then echo "  $s: source absent here, staged copy left as is"; continue; fi
    mkdir -p "$s"
    rsync -a --delete --exclude .git "$src/" "$s/"
    refreshed+=("$s")
    echo "  $s: refreshed ($(git -C "$src" rev-parse --short HEAD 2>/dev/null || echo 'no git') at source)"
done

# ---- scrub: the public snapshot carries no home path, no machine address,
# no account name, no personal address. Patterns in scrub_patterns.tsv.
echo "== scrubbing =="
scrubbed=0
while IFS=$'\t' read -r pat rep; do
    [ -z "$pat" ] && continue; case "$pat" in '#'*) continue ;; esac
    while IFS= read -r f; do
        [ -f "$f" ] || continue
        case "$(file -b --mime-type "$f")" in text/*|application/json|application/x-shellscript|application/javascript) ;; *) continue ;; esac
        sed -i -E "s|$pat|$rep|g" "$f"; scrubbed=$((scrubbed+1))
    done < <(grep -rlE --exclude-dir=.git -- "$pat" "${SOURCES[@]}" 2>/dev/null)
done < scrub_patterns.tsv
echo "  $scrubbed file-pattern replacements"
left=0
while IFS=$'\t' read -r pat rep; do
    [ -z "$pat" ] && continue; case "$pat" in '#'*) continue ;; esac
    n=$(grep -rlE --exclude-dir=.git -- "$pat" "${SOURCES[@]}" 2>/dev/null | wc -l)
    [ "$n" -gt 0 ] && { echo "  STILL PRESENT after scrub: $pat in $n file(s)"; left=$((left+n)); }
done < scrub_patterns.tsv
[ "$left" -gt 0 ] && { echo "  refusing to commit: a pattern survived the scrub (a binary file, or a spelling the pattern misses)"; exit 1; }
echo "  clean: no pattern remains"

git add -A
if git diff --cached --quiet; then echo "  nothing changed since the last staging"; exit 0; fi
n_files=$(git diff --cached --name-only | wc -l)
git commit -q -m "stage $STAMP: ${refreshed[*]} ($n_files files)"
echo "  committed: $(git log --oneline -1)"
if [ "$PUSH" = 1 ]; then git push -q origin "$(git rev-parse --abbrev-ref HEAD)" && echo "  pushed"; else echo "  not pushed (--no-push)"; fi
