#include <stdint.h>
int64_t probe_mulhsu(int64_t a, uint64_t b) { return (int64_t)(((__int128)a * (__int128)(unsigned __int128)b) >> 64); }
