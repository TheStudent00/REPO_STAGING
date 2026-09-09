// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of ucomiss_xmm_xmm_32__flags__go.
// The term's layer-5 text, LITERAL:
//   Concat(fp.to_ieee_bv(fpToFP(Extract(31, 0, v0))), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1))))
package main

import "math"

//go:noinline
func emu_ucomiss_xmm_xmm_32__flags__go(a float32, b float32) uint64 {
	return uint64((uint64(((uint64(uint32(math.Float32bits(a)))) << 32) | (uint64(uint32(math.Float32bits(b)))))))
}

var g0 float32
var g1 float32
var sink interface{}

func main() {
	sink = emu_ucomiss_xmm_xmm_32__flags__go(g0, g1)
	_ = sink
}
