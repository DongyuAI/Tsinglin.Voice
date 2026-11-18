#!/usr/bin/env bash
# usage: _clone.sh <repo-full-name> <target-dir>
repo="$1"; target="$2"
branch=$(curl -sL --max-time 30 "https://api.github.com/repos/${repo}" | python -c "import sys,json;print(json.load(sys.stdin).get('default_branch','main'))" 2>/dev/null)
[ -z "$branch" ] && branch=main
echo "  branch=$branch"
key=$(echo "$target" | tr '/' '_')
tmp="/f/Tsinglin_Voice/_tmp_${key}.zip"
ok=0
for a in 1 2 3; do
  curl -sL --max-time 300 -o "$tmp" "https://codeload.github.com/${repo}/zip/refs/heads/${branch}" && \
  [ -s "$tmp" ] && unzip -tq "$tmp" >/dev/null 2>&1 && { ok=1; break; }
  echo "  download retry $a"
done
if [ "$ok" = 1 ]; then
  stage="/f/Tsinglin_Voice/_stage_${key}"
  rm -rf "$stage" "$target"; mkdir -p "$stage"
  unzip -q "$tmp" -d "$stage" 2>&1
  inner=$(ls -d "$stage"/*/ 2>/dev/null | head -1)
  mkdir -p "$target"
  if [ -n "$inner" ]; then
    cp -a "$inner". "$target"/
  else
    cp -a "$stage"/* "$target"/
  fi
  rm -rf "$stage" "$tmp"
  echo "  OK $(du -sh "$target" 2>/dev/null | cut -f1)"
else
  echo "  FAIL"; rm -f "$tmp"; exit 1
fi
