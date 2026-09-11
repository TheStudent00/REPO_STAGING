// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xor_gpr_gpr_64__flags_high__go__native_first.
//   v0 ^ v1
package main

//go:noinline
func emu_xor_gpr_gpr_64__flags_high__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64((uint64(uint64(a))) ^ (uint64(uint64(b)))))
	return uint64(v0)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_xor_gpr_gpr_64__flags_high__go__native_first(g0, g1)
	_ = sink
}
