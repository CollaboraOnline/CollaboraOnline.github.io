#!/usr/bin/env bash

# Regenerate the Hugo build-instruction pages from the build READMEs in the
# source repository. The README in the source repository is the single source
# of truth for the build steps. For each page this script fetches the README,
# keeps only the text between the build-doc markers, and writes a Hugo page made
# of the page header stub, that build text, and an Edit button that links to the
# README in the source repository. The generated pages must not be edited by
# hand because the next run overwrites them.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Base location to read the source READMEs from. The default reads the raw files
# from the read-only GitHub mirror of the Gerrit monorepo. Set SOURCE_BASE to a
# "file:///absolute/path/to/online" value to generate from a local checkout when
# testing.
SOURCE_BASE="${SOURCE_BASE:-https://raw.githubusercontent.com/CollaboraOnline/online.mirror/main}"

MARKER_START="<!-- build-doc-start -->"
MARKER_END="<!-- build-doc-end -->"

# One line per page. The fields are separated by a pipe:
#   header stub | README path in the source repository | output page | Edit-button link
PAGES=(
  "scripts/build-headers/co-mac.header|macos/README.md|content/post/build-co-mac.md|https://gerrit.collaboraoffice.com/plugins/gitiles/online/+/refs/heads/main/macos/README.md"
  "scripts/build-headers/co-linux.header|qt/README.md|content/post/build-co-linux.md|https://gerrit.collaboraoffice.com/plugins/gitiles/online/+/refs/heads/main/qt/README.md"
  "scripts/build-headers/co-windows.header|windows/coda/README.md|content/post/build-co-windows.md|https://gerrit.collaboraoffice.com/plugins/gitiles/online/+/refs/heads/main/windows/coda/README.md"
  "scripts/build-headers/code-ios.header|ios/README.md|content/post/build-code-ios.md|https://gerrit.collaboraoffice.com/plugins/gitiles/online/+/refs/heads/main/ios/README.md"
  "scripts/build-headers/code-android.header|android/README.md|content/post/build-code-android.md|https://gerrit.collaboraoffice.com/plugins/gitiles/online/+/refs/heads/main/android/README.md"
)

fetch_readme() {
  local path="$1"
  case "$SOURCE_BASE" in
    file://*) cat "${SOURCE_BASE#file://}/$path" ;;
    *)        curl -fsSL "$SOURCE_BASE/$path" ;;
  esac
}

# Print the lines that sit strictly between the start and end markers.
extract_build_doc() {
  awk -v start="$MARKER_START" -v end="$MARKER_END" '
    index($0, start) { inside = 1; next }
    index($0, end)   { inside = 0 }
    inside           { print }
  '
}

for entry in "${PAGES[@]}"; do
  IFS='|' read -r header source output edit_link <<< "$entry"

  readme="$(fetch_readme "$source")"
  body="$(printf '%s\n' "$readme" | extract_build_doc)"

  if [ -z "$body" ]; then
    echo "ERROR: no build-doc markers found in $source" >&2
    exit 1
  fi

  {
    cat "$header"
    printf '\n'
    printf '%s\n' "$body"
    # Close the section only when the header stub opened one. The desktop pages
    # wrap their body in a section; the iOS and Android pages do not.
    if grep -q '<section' "$header"; then
      printf '\n</section>\n'
    fi
    printf '\n{{< edit-button href="%s" name="Edit page" >}}\n' "$edit_link"
  } > "$output"

  echo "Wrote $output from $source"
done
