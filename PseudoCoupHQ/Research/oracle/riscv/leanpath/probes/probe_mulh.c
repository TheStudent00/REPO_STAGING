/* a probe unit for the handful (2026-09-14): the high half of the signed
   128-bit product, the way a c programmer writes it. A test input, not a
   part of the system; the system's own render is pass B. */
#include <stdint.h>
int64_t probe_mulh(int64_t a, int64_t b) { return (int64_t)(((__int128)a * (__int128)b) >> 64); }
