// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first.
//   Concat(4294967295, fp.to_ieee_bv(fpToFPUnsigned(RNE(), v0)))
package main

import "math"

//go:noinline
func emu_fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first(a uint64) uint64 {
	var v0 float32 = float32(uint64(uint64(a)))
	var v1 uint32 = uint32(math.Float32bits(v0))
	var v2 uint64 = (uint64(((uint64(uint32(0xffffffff))) << 32) | (uint64(v1))))
	return uint64(v2)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first(g0)
	_ = sink
}
