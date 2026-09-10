// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of fcvt_s_lu_fpr_gpr_32__freg_fa0__go.
// The term's layer-5 text, LITERAL:
//   Concat(4294967295, fp.to_ieee_bv(fpToFPUnsigned(RNE(), v0)))
package main

import "math"

//go:noinline
func emu_fcvt_s_lu_fpr_gpr_32__freg_fa0__go(a uint64) uint64 {
	return uint64((uint64(((uint64(uint32(0xffffffff))) << 32) | (uint64(uint32(math.Float32bits(float32(uint64(uint64(a))))))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_fcvt_s_lu_fpr_gpr_32__freg_fa0__go(g0)
	_ = sink
}
