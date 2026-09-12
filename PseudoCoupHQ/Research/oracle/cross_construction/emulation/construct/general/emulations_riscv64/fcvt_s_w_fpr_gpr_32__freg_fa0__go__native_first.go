// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fcvt_s_w_fpr_gpr_32__freg_fa0__go__native_first.
//   Concat(4294967295, fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))
package main

import "math"

//go:noinline
func emu_fcvt_s_w_fpr_gpr_32__freg_fa0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 float32 = float32((int32(v0)))
	var v2 uint32 = uint32(math.Float32bits(v1))
	var v3 uint64 = (uint64(((uint64(uint32(0xffffffff))) << 32) | (uint64(v2))))
	return uint64(v3)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_fcvt_s_w_fpr_gpr_32__freg_fa0__go__native_first(g0)
	_ = sink
}
