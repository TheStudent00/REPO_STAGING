#!/bin/bash
# bb2_l14_the_swift_runtime_directories_raw.sh -- task bb2, lane 14: two
# of the swift probe's own commands, re-run with their RAW output.
#
# WHY.  The conventions verifier re-ran lane 1's probe block and read
# two DIFFERS: `ls -1 /persist/swift/usr/lib/swift/linux` and
# `cat /etc/resolv.conf`.  Both are the probe's own rendering, which
# puts `  out: ` in front of every line and, in the log's first draft,
# was also cut down to the one entry the sentence was about -- which is
# a hand-tidied transcript and this line forbids one.  The two commands
# are run here with nothing in front of their output and nothing cut,
# so the log can paste what a re-run produces.
#
#   [1/2] the three commands, raw
#   [2/2] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u
total=2

i=1
echo "[$i/$total] the swift runtime's own directories, and the resolver"
echo "\$ ls -1d /persist/swift/usr/lib/swift/linux/*/"
ls -1d /persist/swift/usr/lib/swift/linux/*/
echo "\$ ls -1 /persist/swift/usr/lib/swift/linux | wc -l"
ls -1 /persist/swift/usr/lib/swift/linux | wc -l
echo "\$ cat /etc/resolv.conf"
cat /etc/resolv.conf

i=2
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
