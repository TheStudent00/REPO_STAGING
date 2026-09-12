// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divu_gpr_gpr_same_64__reg_a0__go__native_first.
//   If(v0 == 0, 18446744073709551615, bvudiv_i(v0, v0))
package main

//go:noinline
func emu_divu_gpr_gpr_same_64__reg_a0__go__native_first(a uint64) uint64 {
	var v1 bool = ((uint64(uint64(a))) == (uint64(uint64(0x0))))
	var v2 uint64 = 0
	if v1 {
		v2 = uint64(0xffffffffffffffff)
	} else {
		var v0 uint64 = (uint64((uint64(uint64(a))) / (uint64(uint64(a)))))
		v2 = v0
	}
	return uint64(v2)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_divu_gpr_gpr_same_64__reg_a0__go__native_first(g0)
	_ = sink
}
