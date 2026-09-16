// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fdiv_s_fpr_fpr_fpr_32__freg_fa0__go__native_first.
//   Concat(4294967295, fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) / fpToFP(Extract(31, 0, v1))))
package main

import "math"

//go:noinline
func emu_fdiv_s_fpr_fpr_fpr_32__freg_fa0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 float32 = math.Float32frombits(uint32(v0))
	var v2 uint32 = uint32(a)
	var v3 float32 = math.Float32frombits(uint32(v2))
	var v4 float32 = ((v3) / (v1))
	var v5 uint32 = uint32(math.Float32bits(v4))
	var v6 uint64 = (uint64(((uint64(uint32(0xffffffff))) << 32) | (uint64(v5))))
	return uint64(v6)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_fdiv_s_fpr_fpr_fpr_32__freg_fa0__go__native_first(g0, g1)
	_ = sink
}
