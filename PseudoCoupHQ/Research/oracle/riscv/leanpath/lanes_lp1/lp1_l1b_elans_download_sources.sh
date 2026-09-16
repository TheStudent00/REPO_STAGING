#!/usr/bin/env bash
# lp1 lane 1b -- lane 1's toolchain install was refused by the proxy
# ("CONNECT tunnel failed, response 403"). This lane names the host elan
# reached for, LITERAL, from elan's own binary and help text, and asks
# whether elan has a documented way to take the same release from
# github.com (an allowlisted host the brief itself names as the source).
# It fetches NOTHING unless that documented way exists; then it tries the
# one install, once, and prints the outcome. No allowlist is edited.
set -u
export PATH=/opt/elan/bin:$PATH
export ELAN_HOME=/persist/lp1/elan
export HOME=/work
total=4
echo "[1/$total] elan's help, LITERAL"
elan --version
elan toolchain install --help 2>&1 | head -40
echo "[2/$total] every URL pattern inside the elan binary, LITERAL"
strings "$(command -v elan)" | grep -i 'lean-lang\|github.com/leanprover\|releases/download\|ELAN_' | sort -u | head -40
echo "[3/$total] the refusal, repeated once with verbose curl-level output"
ELAN_LOG=debug elan toolchain install leanprover/lean4:v4.29.0 2>&1 | tail -20
echo "[4/$total] can the proxy reach github.com at all (the allowlisted host)?"
curl -sS -o /dev/null -w 'github.com: http %{http_code}\n' https://github.com/rems-project/lean-sail 2>&1 | tail -2
curl -sS -o /dev/null -w 'release.lean-lang.org: http %{http_code}\n' https://release.lean-lang.org/ 2>&1 | tail -2
curl -sSI https://github.com/leanprover/lean4/releases/download/v4.29.0/lean-4.29.0-linux.tar.zst 2>&1 | head -5
echo "lane lp1_l1b done"
