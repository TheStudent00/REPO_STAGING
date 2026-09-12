// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of bgeu_gpr_gpr_64__branch_condition__go__native_first.
//   If(ULE(v0, v1), 1, 0)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_bgeu_gpr_gpr_64__branch_condition__go__native_first(a uint64, b uint64) uint64 {
	var v0 bool = (((uint64(uint64(b)))) <= ((uint64(uint64(a)))))
	var v1 uint64 = sel64(v0, uint64(uint64(0x1)), uint64(uint64(0x0)))
	return uint64(v1)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_bgeu_gpr_gpr_64__branch_condition__go__native_first(g0, g1)
	_ = sink
}
