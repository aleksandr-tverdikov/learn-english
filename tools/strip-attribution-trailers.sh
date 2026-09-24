#!/usr/bin/env bash
# Remove Co-Authored-By / Claude-Session trailers from commit messages on the
# current branch, then (with --push) publish the rewritten history.
#
#   tools/strip-attribution-trailers.sh           # check and rewrite locally, no push
#   tools/strip-attribution-trailers.sh --push    # …and force-push with --force-with-lease
#   tools/strip-attribution-trailers.sh --undo    # put the branch back where it was
#
# Rewriting history changes commit hashes, so every other clone of this repo
# needs `git fetch && git reset --hard origin/<branch>` afterwards. Nothing is
# pushed unless you pass --push. A backup branch is made before any rewrite, and
# the script refuses to push if the rewrite changed one byte of file content.
set -euo pipefail

TRAILERS='^(Co-Authored-By|Claude-Session|Co-authored-by): '
BACKUP="backup-before-trailer-strip"
REMOTE="${REMOTE:-origin}"
cd "$(git rev-parse --show-toplevel)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

die() { printf '\n%s\n' "$1" >&2; exit 1; }

if [ "${1:-}" = "--undo" ]; then
    git rev-parse --verify --quiet "$BACKUP" >/dev/null || die "No $BACKUP branch to undo from."
    git reset --hard "$BACKUP"
    echo "Restored $BRANCH to $BACKUP ($(git rev-parse --short HEAD)). The remote is untouched."
    exit 0
fi

# -uno: untracked files are irrelevant to a history rewrite, tracked changes are not
[ -z "$(git status --porcelain -uno)" ] || die "Tracked files have uncommitted changes. Commit or stash first."

# Commits whose message carries a trailer, oldest last.
# portable: macOS ships bash 3.2, which has no mapfile
HITS=()
while IFS= read -r sha; do
    HITS+=("$sha")
done < <(git log --format='%H' "$BRANCH" | while read -r sha; do
    git log --format=%B -n 1 "$sha" | grep -Eq "$TRAILERS" && echo "$sha"
done)

if [ "${#HITS[@]}" -eq 0 ]; then
    echo "No attribution trailers in the history of $BRANCH — nothing to rewrite."
else
    OLDEST="${HITS[${#HITS[@]}-1]}"
    echo "Trailers found in ${#HITS[@]} commit(s); oldest is $(git rev-parse --short "$OLDEST")."
    for sha in "${HITS[@]}"; do git log --format='  %h %s' -n 1 "$sha"; done

    git branch -f "$BACKUP" "$BRANCH"
    echo "Backup branch $BACKUP -> $(git rev-parse --short "$BACKUP")"

    RANGE="$OLDEST^..$BRANCH"
    git rev-parse --verify --quiet "$OLDEST^" >/dev/null || RANGE="$BRANCH"   # trailer in the root commit
    rm -rf .git/refs/original
    FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f \
        --msg-filter "sed -E '/$TRAILERS/d'" "$RANGE" >/dev/null 2>&1
    echo "Rewrote the messages."

    # A message-only rewrite must not touch content. If it did, stop.
    [ -z "$(git diff "$BACKUP" "$BRANCH")" ] || die "ABORT: file content changed. Run with --undo."
    [ "$(git rev-list --count "$BACKUP")" = "$(git rev-list --count "$BRANCH")" ] ||
        die "ABORT: commit count changed. Run with --undo."
    LEFT="$(git log --format=%B "$BRANCH" | grep -Ec "$TRAILERS" || true)"
    [ "$LEFT" = "0" ] || die "ABORT: $LEFT trailer line(s) still present."
    echo "Verified: no trailers left, $(git rev-list --count "$BRANCH") commits, file content byte-identical."
fi

if ! git rev-parse --verify --quiet "$REMOTE/$BRANCH" >/dev/null; then
    echo "No $REMOTE/$BRANCH to compare against. Nothing to push."
    exit 0
fi

if [ "$(git rev-parse "$BRANCH")" = "$(git rev-parse "$REMOTE/$BRANCH")" ]; then
    echo "$REMOTE/$BRANCH already matches $BRANCH. Done."
    exit 0
fi

echo
echo "$BRANCH and $REMOTE/$BRANCH differ:"
echo "  local : $(git rev-parse --short "$BRANCH")"
echo "  remote: $(git rev-parse --short "$REMOTE/$BRANCH")"

if [ "${1:-}" = "--push" ]; then
    git push --force-with-lease "$REMOTE" "$BRANCH"
    echo "Pushed. Other clones now need: git fetch && git reset --hard $REMOTE/$BRANCH"
else
    echo
    echo "Nothing pushed. To publish:   tools/strip-attribution-trailers.sh --push"
    echo "To undo the rewrite:          tools/strip-attribution-trailers.sh --undo"
fi
