"""progress.py -- the shared progress instrument for layer 3.

Standing requirement, CORE 0_3_2 ruling 4 (the owner, 2026-08-18): every
generation phase and every run phase prints [done/total], elapsed and
ETA as it works.

Two faces, deliberately:

  * Progress   -- for host-side python (generators, readers).
  * sh_progress() -- emits the SAME instrument as POSIX shell text, to be
    pasted into a lane script, because a lane cannot import this file
    (the runner cannot see the repo).

Both print to a stream that is line-buffered and flushed on every tick,
so a half-finished lane log is pollable mid-run.  That is the whole
point: a run that prints only at the end is not instrumented.

ETA is from the RUNNING MEAN of completed units, not from a fixed rate
guess.  It is therefore honest early (wide) and tightens as it goes.
"""

import sys
import time


def _hms(seconds):
    if seconds is None or seconds != seconds or seconds < 0:
        return "--:--:--"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return "%02d:%02d:%02d" % (h, m, s)


class Progress:
    """[done/total] + elapsed + ETA, printed on a schedule.

    every -- print at most one line per this many units
    secs  -- ... but always print if this many seconds have passed
    """

    def __init__(self, total, label, every=1000, secs=15.0, stream=None):
        self.total = int(total)
        self.label = label
        self.every = max(1, int(every))
        self.secs = float(secs)
        self.stream = stream or sys.stdout
        self.done = 0
        self.t0 = time.time()
        self.last_n = 0
        self.last_t = self.t0
        self.emit(force=True)

    def tick(self, n=1):
        self.done += n
        now = time.time()
        if (self.done - self.last_n >= self.every
                or now - self.last_t >= self.secs
                or self.done >= self.total):
            self.emit()

    def emit(self, force=False):
        now = time.time()
        elapsed = now - self.t0
        if self.done > 0:
            mean = elapsed / self.done
            eta = mean * (self.total - self.done)
        else:
            mean = 0.0
            eta = None
        pct = (100.0 * self.done / self.total) if self.total else 100.0
        self.stream.write(
            "[progress] %-22s [%d/%d] %5.1f%%  elapsed %s  ETA %s"
            "  mean %.3f ms/unit\n"
            % (self.label, self.done, self.total, pct,
               _hms(elapsed), _hms(eta), mean * 1000.0))
        try:
            self.stream.flush()
        except Exception:
            pass
        self.last_n = self.done
        self.last_t = now

    def close(self):
        if self.done != self.last_n:
            self.emit(force=True)
        elapsed = time.time() - self.t0
        self.stream.write(
            "[progress] %-22s DONE %d units in %s\n"
            % (self.label, self.done, _hms(elapsed)))
        try:
            self.stream.flush()
        except Exception:
            pass


SH_PROGRESS = r'''
# ---- shared progress instrument (from Research/kind_fuzz_clustering/
# progress.py :: SH_PROGRESS).  Prints [done/total], elapsed, ETA from
# the running mean.  Requirement, not a nicety: CORE 0_3_2 ruling 4.
PG_TOTAL=0; PG_DONE=0; PG_T0=0; PG_LABEL=""; PG_EVERY=1; PG_LAST=0
pg_now() { date +%s; }
pg_hms() {
  _s=$1
  printf '%02d:%02d:%02d' $((_s/3600)) $(((_s%3600)/60)) $((_s%60))
}
pg_start() {
  PG_LABEL=$1; PG_TOTAL=$2; PG_EVERY=${3:-1}
  PG_DONE=0; PG_T0=$(pg_now); PG_LAST=0
  echo "[progress] $PG_LABEL [0/$PG_TOTAL] 0.0%  elapsed 00:00:00  ETA --:--:--"
}
pg_tick() {
  PG_DONE=$((PG_DONE+1))
  if [ $((PG_DONE - PG_LAST)) -ge "$PG_EVERY" ] || [ "$PG_DONE" -ge "$PG_TOTAL" ]
  then
    PG_LAST=$PG_DONE
    _el=$(( $(pg_now) - PG_T0 ))
    if [ "$PG_DONE" -gt 0 ]; then
      _eta=$(( _el * (PG_TOTAL - PG_DONE) / PG_DONE ))
    else
      _eta=0
    fi
    _pct=$(( 1000 * PG_DONE / (PG_TOTAL>0?PG_TOTAL:1) ))
    echo "[progress] $PG_LABEL [$PG_DONE/$PG_TOTAL] $((_pct/10)).$((_pct%10))%  elapsed $(pg_hms $_el)  ETA $(pg_hms $_eta)"
  fi
}
pg_done() {
  _el=$(( $(pg_now) - PG_T0 ))
  echo "[progress] $PG_LABEL DONE $PG_DONE units in $(pg_hms $_el)"
}
# ---- end progress instrument
'''


def sh_progress():
    """The POSIX-shell twin, for pasting into a lane script."""
    return SH_PROGRESS


if __name__ == "__main__":
    p = Progress(50, "self-test", every=10, secs=0.2)
    for _ in range(50):
        time.sleep(0.005)
        p.tick()
    p.close()
