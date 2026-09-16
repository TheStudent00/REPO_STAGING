#include <stdint.h>
uint64_t probe_mulhu(uint64_t a, uint64_t b) { return (uint64_t)(((unsigned __int128)a * (unsigned __int128)b) >> 64); }
