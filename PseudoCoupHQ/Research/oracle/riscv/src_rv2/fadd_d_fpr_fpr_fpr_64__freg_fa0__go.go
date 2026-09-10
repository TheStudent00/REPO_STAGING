// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of fadd_d_fpr_fpr_fpr_64__freg_fa0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(v0) + fpToFP(v1))
package main

import "math"

//go:noinline
func emu_fadd_d_fpr_fpr_fpr_64__freg_fa0__go(a uint64, b uint64) uint64 {
	return uint64(uint64(math.Float64bits(((math.Float64frombits(uint64(uint64(a)))) + (math.Float64frombits(uint64(uint64(b))))))))
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_fadd_d_fpr_fpr_fpr_64__freg_fa0__go(g0, g1)
	_ = sink
}
